"""Slow-marked integration test for `authenticated_session` — Basic profile end-to-end."""

from __future__ import annotations

import pytest
from dhis2_core.plugins.browser.service import authenticated_session
from dhis2_core.profile import Profile

pytestmark = pytest.mark.slow


async def test_authenticated_session_basic_lands_in_dashboard_app(
    local_url: str,
    local_username: str,
    local_password: str,
    local_available: bool,
) -> None:
    """End-to-end: Basic profile → mint_jsessionid → Playwright context → dashboard app loads."""
    if not local_available:
        pytest.skip(f"local DHIS2 not reachable at {local_url}")

    profile = Profile(
        base_url=local_url,
        auth="basic",
        username=local_username,
        password=local_password,
    )
    async with authenticated_session(profile, navigate_to="/dhis-web-dashboard/") as (_, page):
        # DHIS2 redirects /dhis-web-dashboard/ into the apps shell.
        assert "/apps/dashboard" in page.url or "/dhis-web-dashboard" in page.url
        title = await page.title()
        assert "DHIS2" in title
