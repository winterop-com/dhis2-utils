"""Minimal dhis2-client example: connect, call /api/me, print the username.

Shows the absolute simplest shape of a dhis2-client usage — no profile
resolution, no generated resources, just pick an auth kind from env and
run one typed query.

Usage:
    uv run python examples/01_whoami.py

Env:
    DHIS2_URL       default http://localhost:8080
    DHIS2_PAT       preferred — a Personal Access Token
    DHIS2_USERNAME / DHIS2_PASSWORD   Basic fallback if no PAT is set
"""

from __future__ import annotations

import asyncio
import os

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    username = os.environ.get("DHIS2_USERNAME", "admin")
    password = os.environ.get("DHIS2_PASSWORD", "district")
    return BasicAuth(username=username, password=password)


async def main() -> None:
    """Connect to DHIS2 and print the authenticated user's identity."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        me = await client.system.me()
        info = await client.system.info()
        print(f"Connected to DHIS2 {info.version} ({info.systemName or 'unnamed'}) at {base_url}")
        print(f"  authenticated as: {me.username} ({me.displayName or '-'})")


if __name__ == "__main__":
    asyncio.run(main())
