"""OAuth 2.1 authorization-code flow with PKCE for DHIS2 OpenID Connect."""

from __future__ import annotations

import asyncio
import base64
import contextlib
import hashlib
import secrets
import time
import urllib.parse
import webbrowser
from collections.abc import Awaitable, Callable
from typing import Any, Protocol, runtime_checkable

import httpx
from pydantic import BaseModel

from dhis2_client.errors import OAuth2FlowError

RedirectCapturer = Callable[[str, str], Awaitable[str]]
"""Callable signature for the redirect-receiver hook.

Takes `(auth_url, expected_state)` and returns the authorization code. The
default implementation in `OAuth2Auth` uses a bare `asyncio.start_server`
loopback handler; `dhis2-core` injects a FastAPI+uvicorn variant via
`build_auth()` so CLI/MCP surfaces get a polished HTML confirmation page.
"""


class OAuth2Token(BaseModel):
    """Access + refresh token pair with expiry info (unix epoch seconds)."""

    access_token: str
    refresh_token: str | None = None
    expires_at: float


@runtime_checkable
class TokenStore(Protocol):
    """Persists OAuth2 tokens across runs — filesystem, keyring, SQLite, etc."""

    async def get(self, key: str) -> OAuth2Token | None:
        """Load tokens for `key` or return None if none stored."""
        ...

    async def set(self, key: str, token: OAuth2Token) -> None:
        """Persist tokens for `key`."""
        ...


class OAuth2Auth:
    """Authorization-code flow with PKCE against DHIS2 /oauth2/* endpoints."""

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        scope: str,
        redirect_uri: str,
        token_store: TokenStore,
        store_key: str | None = None,
        redirect_capturer: RedirectCapturer | None = None,
    ) -> None:
        """Construct the provider.

        `store_key` distinguishes tokens across profiles. `redirect_capturer`
        is an optional callable `(auth_url, expected_state) -> code` that
        replaces the default `asyncio.start_server` loopback implementation
        — `dhis2-core` injects a FastAPI-backed one here for a nicer UX.
        """
        self._base_url = base_url.rstrip("/")
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._redirect_uri = redirect_uri
        self._token_store = token_store
        self._store_key = store_key or f"{base_url}:{client_id}"
        self._token: OAuth2Token | None = None
        self._redirect_capturer = redirect_capturer

    async def headers(self) -> dict[str, str]:
        """Return Authorization: Bearer <access_token>, running interactive flow if needed."""
        await self.refresh_if_needed()
        assert self._token is not None
        return {"Authorization": f"Bearer {self._token.access_token}"}

    async def refresh_if_needed(self) -> None:
        """Load cached token, refresh if close to expiry, run interactive flow if missing."""
        if self._token is None:
            self._token = await self._token_store.get(self._store_key)
        if self._token is None:
            self._token = await self._run_authorization_flow()
        elif self._token.expires_at < time.time() + 60:
            self._token = await self._refresh(self._token)
        await self._token_store.set(self._store_key, self._token)

    async def _run_authorization_flow(self) -> OAuth2Token:
        """Run the browser-based PKCE authorization-code flow."""
        code_verifier = secrets.token_urlsafe(96)
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
        code_challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
        state = secrets.token_urlsafe(16)

        auth_params = {
            "client_id": self._client_id,
            "response_type": "code",
            "redirect_uri": self._redirect_uri,
            "scope": self._scope,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        auth_url = f"{self._base_url}/oauth2/authorize?{urllib.parse.urlencode(auth_params)}"

        capturer = self._redirect_capturer or self._capture_code
        code = await capturer(auth_url, state)
        return await self._exchange_code(code, code_verifier)

    async def _capture_code(self, auth_url: str, expected_state: str) -> str:
        """Open the browser and capture the authorization code from the loopback redirect."""
        parsed = urllib.parse.urlparse(self._redirect_uri)
        host = parsed.hostname or "localhost"
        port = parsed.port or 8000

        loop = asyncio.get_running_loop()
        captured: asyncio.Future[dict[str, str]] = loop.create_future()

        async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            request_line = (await reader.readline()).decode("latin-1")
            while (await reader.readline()).strip():
                pass
            try:
                path = request_line.split(" ", 2)[1]
            except IndexError:
                path = ""
            query = urllib.parse.urlparse(path).query
            params = urllib.parse.parse_qs(query)
            result = {k: v[0] for k, v in params.items() if v}

            body = b"Authentication successful. You can close this window."
            writer.write(b"HTTP/1.1 200 OK\r\n")
            writer.write(b"Content-Type: text/html; charset=utf-8\r\n")
            writer.write(f"Content-Length: {len(body)}\r\n".encode("ascii"))
            writer.write(b"Connection: close\r\n\r\n")
            writer.write(body)
            await writer.drain()
            writer.close()
            with contextlib.suppress(Exception):  # best-effort teardown
                await writer.wait_closed()
            if not captured.done():
                captured.set_result(result)

        server = await asyncio.start_server(handle, host, port)
        try:
            webbrowser.open(auth_url)
            result = await captured
        finally:
            server.close()
            await server.wait_closed()

        if result.get("state") != expected_state:
            raise OAuth2FlowError("state mismatch — possible CSRF")
        code = result.get("code")
        if not code:
            raise OAuth2FlowError("no authorization code returned in redirect")
        return code

    async def _exchange_code(self, code: str, code_verifier: str) -> OAuth2Token:
        """Exchange an authorization code for access+refresh tokens."""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self._redirect_uri,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "code_verifier": code_verifier,
        }
        async with httpx.AsyncClient(follow_redirects=True) as http_client:
            response = await http_client.post(f"{self._base_url}/oauth2/token", data=data)
            response.raise_for_status()
            return self._token_from_response(response.json())

    async def _refresh(self, expired: OAuth2Token) -> OAuth2Token:
        """Refresh tokens using the refresh_token grant.

        Wraps HTTP failures in `OAuth2FlowError` so callers see a clean
        actionable message ("run `dhis2 profile login <name>`") instead of a
        raw `httpx.HTTPStatusError` traceback. The most common case is DHIS2
        rotating its OAuth2 client (volume wiped, client UID reissued) —
        the stored refresh_token no longer matches and DHIS2 returns 400.
        """
        if expired.refresh_token is None:
            raise OAuth2FlowError(
                "access token expired and no refresh_token available — run `dhis2 profile login <name>` to re-authorise"
            )
        data = {
            "grant_type": "refresh_token",
            "refresh_token": expired.refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        async with httpx.AsyncClient(follow_redirects=True) as http_client:
            response = await http_client.post(f"{self._base_url}/oauth2/token", data=data)
        if response.status_code >= 400:
            raise OAuth2FlowError(
                f"token refresh failed ({response.status_code}) — "
                "stored refresh_token rejected by DHIS2. "
                "Run `dhis2 profile login <name>` to re-authorise."
            )
        return self._token_from_response(response.json(), fallback_refresh=expired.refresh_token)

    @staticmethod
    def _token_from_response(data: dict[str, Any], fallback_refresh: str | None = None) -> OAuth2Token:
        """Parse a token-endpoint JSON response into an OAuth2Token."""
        expires_in = float(data.get("expires_in", 3600))
        refresh = data.get("refresh_token") or fallback_refresh
        return OAuth2Token(
            access_token=str(data["access_token"]),
            refresh_token=str(refresh) if refresh else None,
            expires_at=time.time() + expires_in,
        )
