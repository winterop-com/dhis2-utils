"""Unit tests for the hand-written SystemModule (system/info, me)."""

from __future__ import annotations

import httpx
import respx
from dhis2_client import BasicAuth, Dhis2Client


@respx.mock
async def test_system_info_parses_model() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(
            200,
            json={"version": "2.44-SNAPSHOT", "revision": "abc1234", "systemName": "DHIS2 Play"},
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        info = await client.system.info()
    finally:
        await client.close()
    assert info.version == "2.44-SNAPSHOT"
    assert info.revision == "abc1234"
    assert info.systemName == "DHIS2 Play"


@respx.mock
async def test_me_parses_model() -> None:
    respx.get("https://dhis2.example/api/me").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "xY123",
                "username": "system",
                "displayName": "System User",
                "authorities": ["ALL"],
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        me = await client.system.me()
    finally:
        await client.close()
    assert me.id == "xY123"
    assert me.username == "system"
    assert me.authorities == ["ALL"]
