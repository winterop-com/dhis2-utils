"""Connect-time semantics for pinned-version vs auto-detect Dhis2Client."""

from __future__ import annotations

import httpx
import respx
from dhis2w_client import BasicAuth, Dhis2, Dhis2Client


def _auth() -> BasicAuth:
    """Build a placeholder Basic-auth provider for connect tests."""
    return BasicAuth(username="admin", password="district")


@respx.mock
async def test_pinned_connect_skips_system_info_round_trip() -> None:
    """A pinned client must not call /api/system/info on connect."""
    base_redirect = respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))
    info_route = respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.43.0"})
    )
    async with Dhis2Client("https://dhis2.example", auth=_auth(), version=Dhis2.V43) as client:
        assert client.version_key == "v43"
        assert client.raw_version == "v43"
    assert base_redirect.called
    assert not info_route.called


@respx.mock
async def test_unpinned_connect_still_calls_system_info() -> None:
    """An auto-detect client (version=None) reaches /api/system/info on connect."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))
    info_route = respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.43.0"})
    )
    async with Dhis2Client("https://dhis2.example", auth=_auth(), version=None) as client:
        assert client.version_key == "v43"
        assert client.raw_version == "2.43.0"
    assert info_route.called


@respx.mock
async def test_pinned_client_lazy_info_populates_raw_version() -> None:
    """After a pinned connect, `client.system.info()` populates `raw_version` from the server."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))
    info_route = respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.43.0", "revision": "abc123"})
    )
    async with Dhis2Client("https://dhis2.example", auth=_auth(), version=Dhis2.V43) as client:
        # Before any info() call, the property falls back to the pinned major.
        assert client.raw_version == "v43"
        await client.system.info()
        # After info(), it reflects the server-reported value.
        assert client.raw_version == "2.43.0"
    assert info_route.call_count == 1
