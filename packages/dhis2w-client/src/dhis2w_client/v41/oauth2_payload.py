"""OAuth2 client-registration wire payload, v41 shape.

DHIS2 v41 names the client-id property `cid` (renamed to `clientId` on v42
and v43 — BUGS.md #39). Multi-valued fields strictly require arrays on v41:
v42 + v43 also accept comma-separated strings and auto-coerce, but v41
rejects strings with Jackson `MismatchedInputException`. Arrays work
uniformly across all three majors.
"""

from __future__ import annotations

from typing import Any


def build_register_payload(
    *,
    client_id: str,
    client_secret_hash: str,
    redirect_uri: str,
    scope: str,
    display_name: str | None,
    client_settings_json: str,
    token_settings_json: str,
) -> dict[str, Any]:
    """Build the `POST /api/oAuth2Clients` body in v41's wire shape."""
    return {
        "name": display_name or client_id,
        "cid": client_id,
        "clientSecret": client_secret_hash,
        "clientAuthenticationMethods": ["client_secret_basic", "client_secret_post"],
        "authorizationGrantTypes": ["authorization_code", "refresh_token"],
        "redirectUris": [redirect_uri],
        "scopes": [scope],
        "clientSettings": client_settings_json,
        "tokenSettings": token_settings_json,
    }
