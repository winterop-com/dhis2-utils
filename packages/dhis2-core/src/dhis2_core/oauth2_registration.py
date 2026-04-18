"""OAuth2 client registration helpers — POST /api/oAuth2Clients + admin-auth selection."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dhis2_client import BasicAuth, Dhis2Client, PatAuth
from dhis2_client.auth.base import AuthProvider
from pydantic import BaseModel, ConfigDict


class OAuth2ClientCredentials(BaseModel):
    """Credentials produced when registering an OAuth2 client with DHIS2."""

    model_config = ConfigDict(frozen=True)

    uid: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scope: str


class TokenStatus(BaseModel):
    """Status of a profile's persisted OAuth2 tokens."""

    model_config = ConfigDict(frozen=True)

    profile: str
    has_token: bool
    store_path: Path | None
    message: str


async def register_oauth2_client(
    *,
    base_url: str,
    admin_auth: AuthProvider,
    client_id: str,
    client_secret: str,
    redirect_uri: str = "http://localhost:8765",
    scope: str = "ALL",
    display_name: str | None = None,
) -> OAuth2ClientCredentials:
    """POST /api/oAuth2Clients to register a new client; returns the persisted credentials.

    DHIS2 v42 stores the client under metadata — admin creds are required. The
    returned `uid` is the metadata object UID (used to DELETE it later); `client_id`
    and `client_secret` are what OAuth2 flows actually use.
    """
    payload: dict[str, Any] = {
        "name": display_name or client_id,
        "cid": client_id,
        "secret": client_secret,
        "redirectUris": [redirect_uri],
        "grantTypes": ["authorization_code", "refresh_token"],
    }
    async with Dhis2Client(base_url, auth=admin_auth) as client:
        response = await client.post_raw("/api/oAuth2Clients", payload)
    uid = str(response.get("response", {}).get("uid") or response.get("id") or "")
    return OAuth2ClientCredentials(
        uid=uid,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
    )


def build_admin_auth(*, pat: str | None, username: str | None, password: str | None) -> AuthProvider:
    """Select a basic/PAT auth provider from the user-supplied admin credentials."""
    if pat:
        return PatAuth(token=pat)
    if username and password:
        return BasicAuth(username=username, password=password)
    raise ValueError("admin credentials required: pass --admin-pat or --admin-user + --admin-pass")
