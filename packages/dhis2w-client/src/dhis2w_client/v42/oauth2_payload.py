"""OAuth2 client-registration wire payload, v42 shape.

DHIS2 v42 renamed the client-id property to `clientId` (v41 still uses
`cid` — see BUGS.md #39). Multi-valued fields ship as arrays; v42 + v43
also accept comma-separated strings and auto-coerce, but arrays work
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
    """Build the `POST /api/oAuth2Clients` body in v42's wire shape."""
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
