"""Integration-style tests for Dhis2Client using respx-mocked HTTP."""

from __future__ import annotations

import httpx
import pytest
import respx
from dhis2_client import AuthenticationError, BasicAuth, Dhis2ApiError, Dhis2Client
from pydantic import BaseModel


class _Me(BaseModel):
    username: str


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


@respx.mock
async def test_401_openid_mapping_message_includes_actionable_fix() -> None:
    """When DHIS2 issues a valid JWT but rejects user mapping, surface the openId PATCH hint."""
    respx.get("https://dhis2.example/api/me").mock(
        return_value=httpx.Response(
            401,
            text="Unauthorized",
            headers={
                "WWW-Authenticate": (
                    'Bearer error="invalid_token", '
                    "error_description=\"Found no matching DHIS2 user for the mapping claim: 'sub' "
                    "with the value: 'admin'\", "
                    'error_uri="https://tools.ietf.org/html/rfc6750#section-3.1"'
                ),
            },
        )
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        with pytest.raises(AuthenticationError) as exc_info:
            await client.get_raw("/api/me")
    finally:
        await client.close()
    message = str(exc_info.value)
    assert "openId='admin'" in message
    assert "claim='sub'" in message
    assert "/api/users/" in message
    assert "v43" in message


@respx.mock
async def test_401_passes_through_unrecognised_error_description() -> None:
    """For other 401s (e.g. expired token), the error_description is appended verbatim."""
    respx.get("https://dhis2.example/api/me").mock(
        return_value=httpx.Response(
            401,
            text="Unauthorized",
            headers={
                "WWW-Authenticate": 'Bearer error="invalid_token", error_description="Token has expired"',
            },
        )
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        with pytest.raises(AuthenticationError) as exc_info:
            await client.get_raw("/api/me")
    finally:
        await client.close()
    assert "Token has expired" in str(exc_info.value)


async def test_resolve_canonical_base_url_returns_original_when_probe_fails() -> None:
    # No respx mock set up — probe fails, returns original base (defensive fallback).
    resolved = await Dhis2Client._resolve_canonical_base_url("https://dhis2.example")
    assert resolved == "https://dhis2.example"


@respx.mock
async def test_resolve_canonical_base_url_follows_cross_host_redirect() -> None:
    # Simulate play.dhis2.org/dev -> play.im.dhis2.org/dev pattern.
    respx.get("https://play.dhis2.org/dev/").mock(
        return_value=httpx.Response(302, headers={"location": "https://play.im.dhis2.org/dev/"}),
    )
    respx.get("https://play.im.dhis2.org/dev/").mock(
        return_value=httpx.Response(302, headers={"location": "https://play.im.dhis2.org/dev/dhis-web-login/"}),
    )
    respx.get("https://play.im.dhis2.org/dev/dhis-web-login/").mock(
        return_value=httpx.Response(200, text="<html>login</html>"),
    )
    resolved = await Dhis2Client._resolve_canonical_base_url("https://play.dhis2.org/dev")
    # The /dhis-web-login suffix is stripped so we land on the DHIS2 root.
    assert resolved == "https://play.im.dhis2.org/dev"


@respx.mock
async def test_resolve_canonical_base_url_strips_login_suffix() -> None:
    respx.get("http://localhost:8080/").mock(
        return_value=httpx.Response(302, headers={"location": "/dhis-web-login/"}),
    )
    respx.get("http://localhost:8080/dhis-web-login/").mock(
        return_value=httpx.Response(200, text="<html>login</html>"),
    )
    resolved = await Dhis2Client._resolve_canonical_base_url("http://localhost:8080")
    assert resolved == "http://localhost:8080"
