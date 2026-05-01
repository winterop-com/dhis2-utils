"""Live integration tests against https://play.im.dhis2.org/dev. Marked slow."""

from __future__ import annotations

import httpx
import pytest
from dhis2_client import BasicAuth, Dhis2Client, UnsupportedVersionError
from dhis2_client.generated import available_versions

pytestmark = pytest.mark.slow


async def test_play_api_me_returns_user(play_url: str, play_username: str, play_password: str) -> None:
    auth = BasicAuth(username=play_username, password=play_password)
    async with httpx.AsyncClient(base_url=play_url, timeout=httpx.Timeout(30.0, connect=60.0)) as http:
        headers = await auth.headers()
        response = await http.get("/api/me", headers=headers)
    response.raise_for_status()
    body = response.json()
    assert body.get("username") == play_username


async def test_play_system_info_is_reachable(play_url: str, play_username: str, play_password: str) -> None:
    auth = BasicAuth(username=play_username, password=play_password)
    async with httpx.AsyncClient(base_url=play_url, timeout=httpx.Timeout(30.0, connect=60.0)) as http:
        headers = await auth.headers()
        response = await http.get("/api/system/info", headers=headers)
    response.raise_for_status()
    body = response.json()
    assert "version" in body


async def test_play_client_connect_behavior(play_url: str, play_username: str, play_password: str) -> None:
    auth = BasicAuth(username=play_username, password=play_password)
    client = Dhis2Client(play_url, auth=auth)
    try:
        if not available_versions():
            with pytest.raises(UnsupportedVersionError):
                await client.connect()
        else:
            await client.connect()
            assert client.version_key.startswith("v")
    finally:
        await client.close()
