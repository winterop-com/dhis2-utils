"""Service layer for the `browser` plugin — thin wrappers around `dhis2_browser`.

Imports from `dhis2-browser` (the Playwright-carrying workspace member) are
guarded so the plugin stays importable even when the optional `[browser]`
extra isn't installed. The CLI surface substitutes a stub command in that
case; every real call funnels through `require_browser()` here and raises
a clear error if the module is missing.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from importlib.util import find_spec
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
from dhis2_client import BasicAuth

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile

if TYPE_CHECKING:
    from dhis2_browser import CaptureResult, PatOptions
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


async def list_dashboards(profile: Profile) -> list[dict[str, object]]:
    """List every dashboard on the instance — (uid, display name, item count) triples.

    Returns the raw-ish shape `GET /api/dashboards` ships so the caller can
    filter freely before kicking off the (expensive) screenshot loop.
    """
    async with open_client(profile) as client:
        raw = await client.get_raw(
            "/api/dashboards",
            params={"fields": "id,displayName,dashboardItems[id]", "paging": "false"},
        )
    dashboards = raw.get("dashboards")
    if not isinstance(dashboards, list):
        return []
    return [entry for entry in dashboards if isinstance(entry, dict)]


async def capture_dashboards(
    profile: Profile,
    *,
    output_dir: Path,
    only: Sequence[str] | None = None,
    headless: bool | None = None,
    banner: bool = True,
    trim: bool = True,
) -> list[CaptureResult]:
    """Capture full-page PNGs of every (or `only=...`) dashboard for the profile.

    Output PNGs land under `output_dir/<YYYY-MM-DD>-<slug>.png`, one per
    dashboard. Each capture shares the same Playwright context (one login,
    one dashboard-app load) and swaps dashboards via hash navigation, so
    the total wall-clock time scales as O(dashboards) not O(logins).
    """
    require_browser()
    from datetime import UTC, datetime  # noqa: PLC0415 — optional-extra guard

    from dhis2_browser import (  # noqa: PLC0415 — optional-extra guard
        DashboardTarget,
        add_banner,
        capture_dashboard,
        slugify,
        switch_dashboard,
        trim_background,
    )

    if profile.username is None:
        raise BrowserWorkflowNotSupported(
            "Dashboard screenshots need a profile with a resolvable username for the banner. "
            "Use a Basic profile (username + password).",
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    dashboards_raw = await list_dashboards(profile)
    targets: list[DashboardTarget] = []
    for entry in dashboards_raw:
        uid = entry.get("id")
        if not isinstance(uid, str):
            continue
        if only is not None and uid not in only:
            continue
        display_name = entry.get("displayName")
        items = entry.get("dashboardItems")
        item_count = len(items) if isinstance(items, list) else 0
        targets.append(
            DashboardTarget(
                uid=uid,
                display_name=str(display_name) if isinstance(display_name, str) else uid,
                item_count=item_count,
            )
        )

    if not targets:
        return []

    today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
    results: list[CaptureResult] = []
    # Land directly in the dashboard app so the first capture doesn't pay for
    # app-shell initialisation on the way in.
    async with authenticated_session(
        profile,
        headless=headless,
        navigate_to="/dhis-web-dashboard/",
    ) as (_, page):
        for target in targets:
            output_path = output_dir / f"{today}-{slugify(target.display_name)}.png"
            await switch_dashboard(page, target.uid)
            result = await capture_dashboard(page, target, output_path)
            if trim:
                trim_background(output_path)
            if banner:
                add_banner(
                    output_path,
                    target.display_name,
                    instance_url=profile.base_url,
                    username=profile.username,
                    item_count=target.item_count,
                )
            results.append(result)
    return results
