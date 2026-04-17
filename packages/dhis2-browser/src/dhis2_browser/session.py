"""Authenticated Playwright session helpers for DHIS2."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from playwright.async_api import BrowserContext, Page, async_playwright


@asynccontextmanager
async def logged_in_page(
    base_url: str,
    username: str,
    password: str,
    *,
    headless: bool = True,
    timeout_ms: int = 30_000,
) -> AsyncIterator[tuple[BrowserContext, Page]]:
    """Yield an authenticated Playwright `(context, page)` tuple logged into DHIS2.

    Navigates to `{base_url}/dhis-web-login/`, fills the React login form, and
    waits for the post-login redirect. On exit the browser context is closed.
    """
    url = base_url.rstrip("/")
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
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
