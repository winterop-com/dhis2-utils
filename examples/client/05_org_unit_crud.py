"""Full CRUD lifecycle for an organisation unit.

Shows the four verbs against `/api/organisationUnits` — create, read,
update (JSON Patch via `client.patch_raw`), delete — under the seeded
Norway root so nothing leaks into the default DHIS2 hierarchy. Cleans
up even on failure via a try/finally.

The script mints a fresh 11-char UID from `/api/system/id` so reruns
don't collide.

Usage:
    uv run python examples/05_org_unit_crud.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth

PARENT_UID = "NORNorway01"  # seeded in infra/dhis.sql.gz — "Norway"


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


async def _mint_uid(client: Dhis2Client) -> str:
    """Ask DHIS2 for a fresh server-generated UID."""
    response = await client.get_raw("/api/system/id", params={"limit": 1})
    codes = response.get("codes", [])
    return str(codes[0])


async def _dump(label: str, payload: Any) -> None:
    """Print a labelled JSON block."""
    print(f"\n=== {label} ===")
    print(json.dumps(payload, indent=2)[:800])


async def main() -> None:
    """Create, read, patch, delete one org unit under the Norway root."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), pin_version=Dhis2.V42) as client:
        uid = await _mint_uid(client)
        print(f"minted UID: {uid}")

        # CREATE
        new_ou = {
            "id": uid,
            "code": f"EX_OU_{uid}",
            "name": f"Example clinic {uid}",
            "shortName": f"Ex {uid[:6]}",
            "openingDate": "2025-01-01",
            "parent": {"id": PARENT_UID},
        }
        created = await client.post_raw("/api/organisationUnits", new_ou)
        await _dump("CREATE /api/organisationUnits", created.get("response", created))

        try:
            # READ
            fetched = await client.get_raw(
                f"/api/organisationUnits/{uid}",
                params={"fields": "id,code,name,shortName,level,parent[id,name]"},
            )
            await _dump(f"READ /api/organisationUnits/{uid}", fetched)

            # UPDATE — JSON Patch on shortName
            await client.patch_raw(
                f"/api/organisationUnits/{uid}",
                [{"op": "replace", "path": "/shortName", "value": f"Updated {uid[:6]}"}],
            )
            updated = await client.get_raw(
                f"/api/organisationUnits/{uid}",
                params={"fields": "id,shortName,lastUpdated"},
            )
            await _dump(f"PATCH /api/organisationUnits/{uid}", updated)

        finally:
            # DELETE — always, even if one of the steps above failed mid-way.
            deleted = await client.delete_raw(f"/api/organisationUnits/{uid}")
            await _dump(f"DELETE /api/organisationUnits/{uid}", deleted)


if __name__ == "__main__":
    asyncio.run(main())
