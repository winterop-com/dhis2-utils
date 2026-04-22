"""Playwright-driven OAuth2 login — spawn the CLI, drive the IdP form, collect tokens."""

from __future__ import annotations

import asyncio
import os
import re
from pathlib import Path

from playwright.async_api import async_playwright
from pydantic import BaseModel, ConfigDict

from dhis2_browser.session import resolve_headless

_AUTH_URL_HEADER = "Open this URL in a browser to authenticate:"
_AUTH_URL_PATTERN = re.compile(r"https?://\S+")


class OAuth2LoginResult(BaseModel):
    """Outcome of a Playwright-driven `dhis2 profile login --no-browser` run."""

    model_config = ConfigDict(frozen=True)

    profile: str
    auth_url: str
    returncode: int
    stdout: str
    stderr: str


async def drive_oauth2_login(
    profile_name: str,
    *,
    username: str,
    password: str,
    headless: bool | None = None,
    timeout: float = 60.0,
    env: dict[str, str] | None = None,
    cwd: Path | str | None = None,
) -> OAuth2LoginResult:
    """Run `dhis2 profile login <name> --no-browser` end-to-end via Playwright.

    Spawns the CLI as a subprocess, reads the DHIS2 authorize URL from its
    stderr, launches a Chromium instance, navigates to the URL, fills the
    DHIS2 login form with `(username, password)`, and waits for the CLI to
    exit — which happens once the authorization-code redirect hits the
    profile's `redirect_uri` and tokens land in the scope-appropriate
    `tokens.sqlite`.

    The `--no-browser` path is what makes this automatable — the default
    `dhis2 profile login` calls `webbrowser.open(url)` against the system
    browser, which Chromium can't see. See `docs/architecture/auth.md` for
    the flag's manual-use cases.

    `headless=None` honours the `DHIS2_HEADFUL=1` env fallback (matches
    the other `dhis2-browser` helpers). `timeout` bounds the whole flow
    including the subprocess wait.

    Raises `RuntimeError` on: missing auth URL in stderr, Playwright
    failure (login-form selector drift, network), subprocess timeout,
    or non-zero CLI exit.
    """
    command = ["dhis2", "profile", "login", profile_name, "--no-browser"]
    merged_env = {**os.environ, **(env or {})}
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=merged_env,
        cwd=str(cwd) if cwd else None,
    )
    stderr_buffer: list[str] = []
    try:
        auth_url = await asyncio.wait_for(_read_auth_url(proc, stderr_buffer), timeout=timeout)
    except TimeoutError as exc:
        proc.kill()
        await proc.wait()
        raise RuntimeError(
            f"timed out after {timeout}s waiting for `dhis2 profile login` to emit the authorize URL",
        ) from exc

    try:
        await asyncio.wait_for(
            _drive_login_form(auth_url, username=username, password=password, headless=resolve_headless(headless)),
            timeout=timeout,
        )
    except Exception:
        proc.kill()
        await proc.wait()
        raise

    try:
        stdout_raw, stderr_raw = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except TimeoutError as exc:
        proc.kill()
        await proc.wait()
        raise RuntimeError(
            f"`dhis2 profile login` did not exit within {timeout}s after the IdP form was submitted "
            "— the redirect receiver may not have captured the code",
        ) from exc

    stdout_text = stdout_raw.decode(errors="replace")
    stderr_text = "".join(stderr_buffer) + stderr_raw.decode(errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(
            f"`dhis2 profile login {profile_name} --no-browser` exited with code {proc.returncode}:\n{stderr_text}",
        )
    return OAuth2LoginResult(
        profile=profile_name,
        auth_url=auth_url,
        returncode=proc.returncode,
        stdout=stdout_text,
        stderr=stderr_text,
    )


async def _read_auth_url(proc: asyncio.subprocess.Process, buffer: list[str]) -> str:
    """Stream stderr until we see the `Open this URL ...` header; return the URL on the next line."""
    assert proc.stderr is not None
    saw_header = False
    while True:
        line_bytes = await proc.stderr.readline()
        if not line_bytes:
            raise RuntimeError(f"`dhis2 profile login` exited before emitting an authorize URL:\n{''.join(buffer)}")
        line = line_bytes.decode(errors="replace")
        buffer.append(line)
        stripped = line.strip()
        if _AUTH_URL_HEADER in stripped:
            saw_header = True
            continue
        if saw_header:
            match = _AUTH_URL_PATTERN.search(stripped)
            if match is not None:
                return match.group(0)


async def _drive_login_form(auth_url: str, *, username: str, password: str, headless: bool) -> None:
    """Launch Chromium, navigate to the authorize URL, fill the DHIS2 login form + consent screen."""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
        context = await browser.new_context()
        try:
            page = await context.new_page()
            await page.goto(auth_url, wait_until="domcontentloaded")
            await page.fill("input[name='username']", username)
            await page.fill("input[name='password']", password)
            await page.click("button[type='submit']")
            # DHIS2 v42 Spring AS serves a "Consent required" screen on the first
            # authorization for a given (user, client, scope) — the user must tick
            # the scope checkbox and click `#submit-consent` for the flow to
            # issue the authorization-code redirect. Subsequent logins with the
            # same tuple skip the consent page and redirect straight to the
            # receiver, so we wait for either terminal state.
            try:
                await page.wait_for_selector("#submit-consent", timeout=10_000)
                await page.check("input[name='scope'][value='ALL']")
                await page.click("#submit-consent")
            except Exception:
                # No consent screen — already-consented path. The authorize
                # endpoint has already fired the redirect, so page.wait_for_url
                # below will hit the receiver origin.
                pass
            # Wait for the browser to arrive at the loopback receiver. At that
            # point the CLI's FastAPI handler has the code and `proc.communicate`
            # on the outer helper will see the subprocess exit cleanly.
            await page.wait_for_url(
                lambda current: current.startswith("http://localhost:") or "8765" in current,
                timeout=15_000,
            )
        finally:
            await context.close()
            await browser.close()
