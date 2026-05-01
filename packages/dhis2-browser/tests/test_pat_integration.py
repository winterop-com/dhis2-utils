"""Slow-marked integration test for `create_pat` — mints a PAT + round-trips via PatAuth."""

from __future__ import annotations

import pytest
from dhis2_browser import PatOptions, create_pat
from dhis2_client import Dhis2Client, PatAuth

pytestmark = pytest.mark.slow


async def test_create_pat_round_trips_through_pat_auth(
    local_url: str,
    local_username: str,
    local_password: str,
    local_available: bool,
) -> None:
    """End-to-end: drive the login form, mint a PAT, authenticate on /api/me with it."""
    if not local_available:
        pytest.skip(f"local DHIS2 not reachable at {local_url}")

    token = await create_pat(
        local_url,
        local_username,
        local_password,
        options=PatOptions(name="dhis2-browser-integration-test", expires_in_days=1),
    )
    assert token.startswith("d2p_"), f"unexpected token prefix: {token[:6]}..."

    async with Dhis2Client(local_url, auth=PatAuth(token=token)) as client:
        me = await client.system.me()
        assert me.username == local_username
