"""OAuth2 client registration helpers — POST /api/oAuth2Clients + admin-auth selection."""

from __future__ import annotations

from typing import Any

import bcrypt
from dhis2w_client import BasicAuth, Dhis2Client, PatAuth
from dhis2w_client.auth.base import AuthProvider
from dhis2w_client.auth.oauth2 import DEFAULT_REDIRECT_URI
from pydantic import BaseModel, ConfigDict

_OAUTH2_CLIENT_AUTH_METHODS = "client_secret_basic,client_secret_post"
_OAUTH2_GRANT_TYPES = "authorization_code,refresh_token"
# Spring Authorization Server serialises ClientSettings / TokenSettings as Jackson JSON
# text columns. Leaving them empty triggers IllegalArgumentException inside
# `Dhis2OAuth2ClientServiceImpl.toObject` when Spring AS tries to rebuild a
# RegisteredClient. These defaults mirror what DHIS2's built-in settings app
# (/apps/settings#/oauth2) writes when a client is created via the UI.
_OAUTH2_CLIENT_SETTINGS_JSON = (
    '{"@class":"java.util.Collections$UnmodifiableMap",'
    '"settings.client.require-proof-key":false,'
    '"settings.client.require-authorization-consent":true}'
)
_OAUTH2_TOKEN_SETTINGS_JSON = (
    '{"@class":"java.util.Collections$UnmodifiableMap",'
    '"settings.token.reuse-refresh-tokens":true,'
    '"settings.token.x509-certificate-bound-access-tokens":false,'
    '"settings.token.id-token-signature-algorithm":'
    '["org.springframework.security.oauth2.jose.jws.SignatureAlgorithm","RS256"],'
    '"settings.token.access-token-time-to-live":["java.time.Duration",300.000000000],'
    '"settings.token.access-token-format":'
    '{"@class":"org.springframework.security.oauth2.server.authorization.settings.OAuth2TokenFormat",'
    '"value":"self-contained"},'
    '"settings.token.refresh-token-time-to-live":["java.time.Duration",3600.000000000],'
    '"settings.token.authorization-code-time-to-live":["java.time.Duration",300.000000000],'
    '"settings.token.device-code-time-to-live":["java.time.Duration",300.000000000]}'
)


class OAuth2ClientCredentials(BaseModel):
    """Credentials produced when registering an OAuth2 client with DHIS2."""

    model_config = ConfigDict(frozen=True)

    uid: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scope: str


def _bcrypt_hash(plaintext: str) -> str:
    """BCrypt-hash `plaintext` for DHIS2's `clientSecret` column.

    DHIS2 wires a `BCryptPasswordEncoder` into Spring Authorization Server's
    client-authentication filter, so a plaintext clientSecret in this TEXT
    column always fails /oauth2/token with 401 invalid_client.
    """
    return bcrypt.hashpw(plaintext.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode("ascii")


async def register_oauth2_client(
    *,
    base_url: str,
    admin_auth: AuthProvider,
    client_id: str,
    client_secret: str,
    redirect_uri: str = DEFAULT_REDIRECT_URI,
    scope: str = "ALL",
    display_name: str | None = None,
) -> OAuth2ClientCredentials:
    """POST /api/oAuth2Clients to register a new client; returns the persisted credentials.

    DHIS2 v42 stores the client under metadata — admin creds are required. The
    returned `uid` is the metadata object UID (used to DELETE it later); `client_id`
    and `client_secret` are what OAuth2 flows use (the plaintext `client_secret`
    is returned here; DHIS2 persists a BCrypt hash and matches at /oauth2/token).
    """
    payload: dict[str, Any] = {
        "name": display_name or client_id,
        "clientId": client_id,
        "clientSecret": _bcrypt_hash(client_secret),
        "clientAuthenticationMethods": _OAUTH2_CLIENT_AUTH_METHODS,
        "authorizationGrantTypes": _OAUTH2_GRANT_TYPES,
        "redirectUris": redirect_uri,
        "scopes": scope,
        "clientSettings": _OAUTH2_CLIENT_SETTINGS_JSON,
        "tokenSettings": _OAUTH2_TOKEN_SETTINGS_JSON,
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
    raise ValueError("admin credentials required: set DHIS2_ADMIN_PAT or DHIS2_ADMIN_PASSWORD (+ --admin-user) in env")
