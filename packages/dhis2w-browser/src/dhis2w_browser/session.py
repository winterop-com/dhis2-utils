"""Authenticated Playwright session helpers for DHIS2."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from playwright.async_api import BrowserContext, Page, async_playwright


def resolve_headless(explicit: bool | None = None) -> bool:
    """Decide whether to run the browser headlessly.

    Precedence: explicit kwarg > `DHIS2_HEADFUL=1` env var (visible) > headless default.
    """
    if explicit is not None:
        return explicit
    env = os.environ.get("DHIS2_HEADFUL", "").strip().lower()
    return env not in {"1", "true", "yes", "on"}


@asynccontextmanager
async def logged_in_page(
    base_url: str,
    username: str,
    password: str,
    *,
    headless: bool | None = None,
    timeout_ms: int = 30_000,
) -> AsyncGenerator[tuple[BrowserContext, Page]]:
    """Yield an authenticated Playwright `(context, page)` tuple logged into DHIS2.

    Navigates to `{base_url}/dhis-web-login/`, fills the React login form, and
    waits for the post-login redirect. On exit the browser context is closed.

    Prefer `session_from_cookie(...)` when you already have a `JSESSIONID` —
    it skips the form interaction entirely. This helper is the fallback for
    flows that genuinely need the React login to happen (e.g. minting a PAT
    on an instance where Basic API auth is disabled).
    """
    url = base_url.rstrip("/")
    resolved_headless = resolve_headless(headless)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=resolved_headless)
        context = await browser.new_context()
        try:
            page = await context.new_page()
            await page.goto(f"{url}/dhis-web-login/", timeout=timeout_ms)
            await page.fill("input[name='username']", username)
            await page.fill("input[name='password']", password)
            await page.click("button[type='submit']")
            await page.wait_for_url(
                lambda current: "/dhis-web-login" not in current,
                timeout=timeout_ms,
            )
            yield context, page
        finally:
            await context.close()
            await browser.close()


@asynccontextmanager
async def session_from_cookie(
    base_url: str,
    jsessionid: str,
    *,
    headless: bool | None = None,
    navigate_to: str | None = None,
    timeout_ms: int = 30_000,
) -> AsyncGenerator[tuple[BrowserContext, Page]]:
    """Yield a Playwright `(context, page)` with a pre-minted `JSESSIONID` cookie injected.

    Caller is expected to have obtained `jsessionid` via a cheap HTTP call
    (e.g. `GET /api/me` with `Authorization: Basic`) — DHIS2 sets the cookie
    in the response's `Set-Cookie` header on any authenticated request. No
    React login form interaction happens here, which makes this flow fast,
    fully headless-friendly, and independent of form-selector drift.

    `navigate_to` picks the landing URL (defaults to `/` — DHIS2 redirects to
    the apps shell). Pass e.g. `/dhis-web-dashboard/` to land directly in
    the dashboard app.
    """
    url = base_url.rstrip("/")
    resolved_headless = resolve_headless(headless)
    landing = navigate_to or "/"
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=resolved_headless)
        context = await browser.new_context()
        await context.add_cookies(
            [
                {
                    "name": "JSESSIONID",
                    "value": jsessionid,
                    "url": url,
                },
            ],
        )
        try:
            page = await context.new_page()
            await page.goto(f"{url}{landing}", timeout=timeout_ms)
            yield context, page
        finally:
            await context.close()
            await browser.close()
