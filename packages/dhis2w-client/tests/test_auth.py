"""Unit tests for the bundled auth providers."""

from __future__ import annotations

import base64
import time

import httpx
import respx
from dhis2w_client.auth.basic import BasicAuth
from dhis2w_client.auth.oauth2 import OAuth2Auth, OAuth2Token
from dhis2w_client.auth.pat import PatAuth


async def test_basic_auth_header() -> None:
    provider = BasicAuth(username="admin", password="district")
    encoded = base64.b64encode(b"admin:district").decode()
    assert await provider.headers() == {"Authorization": f"Basic {encoded}"}


async def test_pat_auth_header() -> None:
    provider = PatAuth(token="d2pat_example")
    assert await provider.headers() == {"Authorization": "ApiToken d2pat_example"}


async def test_basic_refresh_is_noop() -> None:
    await BasicAuth(username="a", password="b").refresh_if_needed()


async def test_pat_refresh_is_noop() -> None:
    await PatAuth(token="t").refresh_if_needed()


class _InMemoryTokenStore:
    """Minimal TokenStore implementation for unit tests."""

    def __init__(self) -> None:
        self._items: dict[str, OAuth2Token] = {}

    async def get(self, key: str) -> OAuth2Token | None:
        return self._items.get(key)

    async def set(self, key: str, token: OAuth2Token) -> None:
        self._items[key] = token


@respx.mock
async def test_oauth2_uses_cached_token_without_interactive_flow() -> None:
    token_store = _InMemoryTokenStore()
    cached = OAuth2Token(access_token="cached-access", refresh_token="cached-refresh", expires_at=time.time() + 3600)
    await token_store.set("profile:prod", cached)

    provider = OAuth2Auth(
        base_url="https://dhis2.example",
        client_id="dhis2-utils",
        client_secret="secret",
        scope="openid email",
        redirect_uri="http://localhost:8765",
        token_store=token_store,
        store_key="profile:prod",
    )
    headers = await provider.headers()
    assert headers == {"Authorization": "Bearer cached-access"}


@respx.mock
async def test_oauth2_refresh_on_near_expiry() -> None:
    token_store = _InMemoryTokenStore()
    expiring = OAuth2Token(access_token="old", refresh_token="refresh-me", expires_at=time.time() + 5)
    await token_store.set("profile:prod", expiring)

    respx.post("https://dhis2.example/oauth2/token").mock(
        return_value=httpx.Response(
            200,
            json={"access_token": "new-access", "refresh_token": "new-refresh", "expires_in": 3600},
        )
    )

    provider = OAuth2Auth(
        base_url="https://dhis2.example",
        client_id="dhis2-utils",
        client_secret="secret",
        scope="openid",
        redirect_uri="http://localhost:8765",
        token_store=token_store,
        store_key="profile:prod",
    )
    headers = await provider.headers()
    assert headers == {"Authorization": "Bearer new-access"}

    stored = await token_store.get("profile:prod")
    assert stored is not None
    assert stored.access_token == "new-access"
    assert stored.refresh_token == "new-refresh"
