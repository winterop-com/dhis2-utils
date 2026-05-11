"""OAuth2 client-registration wire payload, v43 shape.

DHIS2 v43 carries the same `clientId` property + array-typed multi-valued
fields as v42 (v41 still uses `cid` — see BUGS.md #39). Held as its own
file in the v43 tree so future v43-only payload tweaks land here without
touching the v42 sibling.
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
    """Build the `POST /api/oAuth2Clients` body in v43's wire shape."""
    return {
        "name": display_name or client_id,
        "clientId": client_id,
        "clientSecret": client_secret_hash,
        "clientAuthenticationMethods": ["client_secret_basic", "client_secret_post"],
        "authorizationGrantTypes": ["authorization_code", "refresh_token"],
        "redirectUris": [redirect_uri],
        "scopes": [scope],
        "clientSettings": client_settings_json,
        "tokenSettings": token_settings_json,
    }
