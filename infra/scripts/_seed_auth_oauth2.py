"""Standard OAuth2 client seeded by `seed_auth.py`. Edit to change the client config.

Deterministic values so tests and manual exploration can rely on them. Re-running
the seed overwrites the existing client (by clientId lookup) instead of creating
duplicates.
"""

from __future__ import annotations

from typing import Any

OAUTH2_CLIENT_ID = "dhis2-utils-local"
OAUTH2_CLIENT_SECRET = "dhis2-utils-local-secret-do-not-use-in-prod"  # noqa: S105 — local only
OAUTH2_REDIRECT_URI = "http://localhost:8765"
OAUTH2_SCOPES = "openid email ALL"
OAUTH2_GRANT_TYPES = "authorization_code,refresh_token"


def oauth2_payload() -> dict[str, Any]:
    """Return the POST/PUT body accepted by /api/oAuth2Clients."""
    return {
        "name": OAUTH2_CLIENT_ID,
        "clientId": OAUTH2_CLIENT_ID,
        "clientSecret": OAUTH2_CLIENT_SECRET,
        "authorizationGrantTypes": OAUTH2_GRANT_TYPES,
        "redirectUris": OAUTH2_REDIRECT_URI,
        "scopes": OAUTH2_SCOPES,
    }
