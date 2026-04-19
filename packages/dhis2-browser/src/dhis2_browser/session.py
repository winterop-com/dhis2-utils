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
