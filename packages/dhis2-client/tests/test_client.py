"""Integration-style tests for Dhis2Client using respx-mocked HTTP."""

from __future__ import annotations

import httpx
import pytest
import respx
from dhis2_client import AuthenticationError, BasicAuth, Dhis2ApiError, Dhis2Client, UnsupportedVersionError
from dhis2_client.generated import available_versions
from pydantic import BaseModel


class _Me(BaseModel):
    username: str


@respx.mock
async def test_connect_raises_when_version_not_generated() -> None:
    # Use v99 — guaranteed to not have a generated module.
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.99.0"})
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    with pytest.raises(UnsupportedVersionError) as exc:
        await client.connect()
    assert "2.99.0" in str(exc.value)
    await client.close()


@respx.mock
async def test_connect_falls_back_to_nearest_lower_version() -> None:
    available = available_versions()
    if not available:
        pytest.skip("no generated versions available — nothing to fall back to")
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.99.0"}),
    )
    client = Dhis2Client(
        "https://dhis2.example", auth=BasicAuth(username="a", password="b"), allow_version_fallback=True
    )
    try:
        await client.connect()
        # v99 → picks the highest generated version <= 99 (e.g. v42 or v44).
        assert client.version_key in available
        assert int(client.version_key[1:]) <= 99
    finally:
        await client.close()


@respx.mock
async def test_get_raw_injects_auth_header_and_parses_json() -> None:
    route = respx.get("https://dhis2.example/api/me").mock(
        return_value=httpx.Response(200, json={"username": "admin"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="admin", password="district"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        body = await client.get_raw("/api/me")
    finally:
        await client.close()
    assert body == {"username": "admin"}
    assert route.called
    sent_headers = dict(route.calls.last.request.headers)
    assert "authorization" in sent_headers
    assert sent_headers["authorization"].startswith("Basic ")


@respx.mock
async def test_typed_get_returns_pydantic_instance() -> None:
    respx.get("https://dhis2.example/api/me").mock(
        return_value=httpx.Response(200, json={"username": "admin"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="admin", password="district"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        me = await client.get("/api/me", model=_Me)
    finally:
        await client.close()
    assert isinstance(me, _Me)
    assert me.username == "admin"


@respx.mock
async def test_non_success_raises_dhis2_api_error() -> None:
    respx.get("https://dhis2.example/api/missing").mock(
        return_value=httpx.Response(404, json={"message": "not found"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        with pytest.raises(Dhis2ApiError) as exc:
            await client.get_raw("/api/missing")
    finally:
        await client.close()
    assert exc.value.status_code == 404
    assert exc.value.body == {"message": "not found"}


@respx.mock
async def test_401_raises_authentication_error() -> None:
    respx.get("https://dhis2.example/api/me").mock(return_value=httpx.Response(401, text="Unauthorized"))
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        with pytest.raises(AuthenticationError):
            await client.get_raw("/api/me")
    finally:
        await client.close()
