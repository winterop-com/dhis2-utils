"""Service layer for the `browser` plugin — thin wrappers around `dhis2_browser`.

Imports from `dhis2-browser` (the Playwright-carrying workspace member) are
guarded so the plugin stays importable even when the optional `[browser]`
extra isn't installed. The CLI surface substitutes a stub command in that
case; every real call funnels through `require_browser()` here and raises
a clear error if the module is missing.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from importlib.util import find_spec
from typing import TYPE_CHECKING

import httpx
from dhis2_client import BasicAuth

from dhis2_core.profile import Profile

if TYPE_CHECKING:
    from dhis2_browser import PatOptions
    from playwright.async_api import BrowserContext, Page


class BrowserExtraNotInstalled(RuntimeError):
    """Raised when a `browser` command runs without the `[browser]` extra."""


class BrowserWorkflowNotSupported(RuntimeError):
    """Raised when a profile's auth type can't drive a Playwright session.

    PAT profiles hit this: DHIS2 PATs are stateless and never mint a
    `JSESSIONID`, so there's no cookie to inject into the browser. The
    workaround is to use a Basic (or OIDC, once wired) profile for
    browser-driven workflows.
    """


def require_browser() -> None:
    """Confirm `dhis2_browser` is importable; otherwise raise an install hint."""
    if find_spec("dhis2_browser") is None:
        raise BrowserExtraNotInstalled(
            "The `dhis2 browser` commands need the Playwright extra. "
            'Install with `uv pip install "dhis2-cli[browser]"` '
            "(or `uv pip install dhis2-browser`), then run "
            "`playwright install chromium` once to pull the driver.",
        )


async def create_pat(
    url: str,
    username: str,
    password: str,
    *,
    options: PatOptions | None = None,
    headless: bool | None = None,
) -> str:
    """Mint a DHIS2 Personal Access Token V2 via an authenticated browser session."""
    require_browser()
    from dhis2_browser import create_pat as _create_pat  # noqa: PLC0415 — optional-extra guard

    return await _create_pat(url, username, password, options=options, headless=headless)


async def mint_jsessionid(profile: Profile) -> str:
    """Hit `GET /api/me` with the profile's credentials; return the minted JSESSIONID.

    Basic profiles produce a session cookie in the response `Set-Cookie`
    header on any authenticated request. OIDC is expected to behave the
    same way with `Authorization: Bearer <access_token>` but hasn't been
    wired yet — raises `NotImplementedError` for now. PAT profiles raise
    `BrowserWorkflowNotSupported` because PATs are stateless in DHIS2.
    """
    if profile.auth == "pat":
        raise BrowserWorkflowNotSupported(
            "PAT profiles cannot drive browser workflows — DHIS2 PATs are stateless "
            "and do not mint a JSESSIONID cookie. Use a Basic profile (username + "
            "password) for dashboard screenshots, maintenance-app driving, and "
            "other Playwright-based flows.",
        )
    if profile.auth == "oauth2":
        raise NotImplementedError(
            "OIDC browser sessions aren't wired yet — needs a smoke test to confirm "
            "DHIS2 mints a JSESSIONID when `Authorization: Bearer` is presented on "
            "/api/me. Track progress on roadmap Strategic option #4.",
        )
    if profile.username is None or profile.password is None:
        raise BrowserWorkflowNotSupported(
            f"Profile auth={profile.auth!r} has no username/password; cannot mint a JSESSIONID without credentials.",
        )
    auth = BasicAuth(username=profile.username, password=profile.password)
    async with httpx.AsyncClient(base_url=profile.base_url.rstrip("/")) as http_client:
        response = await http_client.get("/api/me", headers=await auth.headers())
        response.raise_for_status()
        jsessionid = response.cookies.get("JSESSIONID")
        if not jsessionid:
            raise RuntimeError(
                "DHIS2 did not return a JSESSIONID cookie on /api/me. Check that "
                "Basic auth is enabled on this instance.",
            )
        return jsessionid


@asynccontextmanager
async def authenticated_session(
    profile: Profile,
    *,
    headless: bool | None = None,
    navigate_to: str | None = None,
) -> AsyncGenerator[tuple[BrowserContext, Page]]:
    """Yield a Playwright `(context, page)` authenticated as the profile's user.

    Mints a `JSESSIONID` from the profile's credentials (via `mint_jsessionid`)
    and injects it into a fresh browser context — no React login form
    interaction required. Raises `BrowserWorkflowNotSupported` for profile
    auth types that can't produce a session (PAT today).
    """
    require_browser()
    from dhis2_browser import session_from_cookie  # noqa: PLC0415 — optional-extra guard

    jsessionid = await mint_jsessionid(profile)
    async with session_from_cookie(
        profile.base_url,
        jsessionid,
        headless=headless,
        navigate_to=navigate_to,
    ) as (context, page):
        yield context, page
