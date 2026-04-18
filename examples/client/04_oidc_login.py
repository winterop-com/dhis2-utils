"""Interactive OAuth 2.1 authorization-code flow with PKCE.

Shows how to stand up `OAuth2Auth` directly (no profile, no plugin).
`dhis2-core` injects a FastAPI-backed redirect receiver via
`redirect_capturer`; this example reuses it so the first run opens a
browser, captures the redirect, and writes tokens to a local SQLite store.

Subsequent runs reuse the cached tokens (and silently refresh when they
near expiry). Delete `./tokens.sqlite` to force a fresh flow.

Usage (against `make dhis2-run`):
    set -a; source infra/home/credentials/.env.auth; set +a
    uv run python examples/04_oauth2_login.py

Env:
    DHIS2_URL                     default http://localhost:8080
    DHIS2_OAUTH_CLIENT_ID         from .env.auth
    DHIS2_OAUTH_CLIENT_SECRET     from .env.auth
    DHIS2_OAUTH_REDIRECT_URI      default http://localhost:8765
    DHIS2_OAUTH_SCOPES            default ALL
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from dhis2_client import Dhis2, Dhis2Client
from dhis2_client.auth.oauth2 import OAuth2Auth
from dhis2_core.oauth2_redirect import capture_code
from dhis2_core.token_store import SqliteTokenStore


async def main() -> None:
    """Run the OAuth2 flow (on first run) and call /api/me with the resulting access token."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    client_id = os.environ["DHIS2_OAUTH_CLIENT_ID"]
    client_secret = os.environ["DHIS2_OAUTH_CLIENT_SECRET"]
    redirect_uri = os.environ.get("DHIS2_OAUTH_REDIRECT_URI", "http://localhost:8765")
    scope = os.environ.get("DHIS2_OAUTH_SCOPES", "ALL")
    token_store = SqliteTokenStore(Path("./tokens.sqlite"))

    async def capturer(auth_url: str, expected_state: str) -> str:
        return await capture_code(redirect_uri, expected_state, open_url=auth_url)

    auth = OAuth2Auth(
        base_url=base_url,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        redirect_uri=redirect_uri,
        token_store=token_store,
        store_key="examples:04_oauth2",
        redirect_capturer=capturer,
    )
    try:
        async with Dhis2Client(base_url, auth=auth, pin_version=Dhis2.V42) as client:
            me = await client.system.me()
            print(f"OAuth2 login ok — authenticated as {me.username} ({me.displayName or '-'})")
    finally:
        await token_store.close()


if __name__ == "__main__":
    asyncio.run(main())
