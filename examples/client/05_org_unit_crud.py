"""Full CRUD lifecycle for an organisation unit.

Shows the four verbs on the typed `client.resources.organisation_units`
accessor — `create`, `get`, `update` (PUT with the whole object), and
`delete` — plus a JSON-Patch update via the escape-hatch `patch_raw`
for the DHIS2 operations the generator doesn't cover yet. Cleans up
even on failure via a try/finally.

The script mints a fresh 11-char UID from `/api/system/id` so reruns
don't collide.

Usage:
    uv run python examples/05_org_unit_crud.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth
from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.schemas.organisation_unit import OrganisationUnit

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
    """Ask DHIS2 for a fresh server-generated UID.

    `/api/system/id` is a utility endpoint, not a resource, so this stays
    on the raw escape hatch.
    """
    response = await client.get_raw("/api/system/id", params={"limit": 1})
    codes = response.get("codes", [])
    return str(codes[0])


async def main() -> None:
    """Create, read, patch, delete one org unit under the Norway root."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        uid = await _mint_uid(client)
        print(f"minted UID: {uid}")

        new_ou = OrganisationUnit(
            id=uid,
            code=f"EX_OU_{uid}",
            name=f"Example clinic {uid}",
            shortName=f"Ex {uid[:6]}",
            openingDate=datetime(2025, 1, 1),
            parent=Reference(id=PARENT_UID),
        )
        created = await client.resources.organisation_units.create(new_ou)
        print(f"\nCREATE  {created.get('status', '?')}  uid={uid}")

        try:
            fetched = await client.resources.organisation_units.get(
                uid,
                fields="id,code,name,shortName,level,parent[id,name]",
            )
            print(f"READ    id={fetched.id}  name={fetched.name}  shortName={fetched.shortName}")

            # JSON Patch — use patch_raw because the typed accessor models full PUT,
            # not partial patches. The raw body here is a well-typed pydantic-free
            # JSON Patch array (RFC 6902).
            await client.patch_raw(
                f"/api/organisationUnits/{uid}",
                [{"op": "replace", "path": "/shortName", "value": f"Updated {uid[:6]}"}],
            )
            updated = await client.resources.organisation_units.get(uid, fields="id,shortName,lastUpdated")
            print(f"PATCH   shortName={updated.shortName}  lastUpdated={updated.lastUpdated}")
        finally:
            deleted = await client.resources.organisation_units.delete(uid)
            print(f"\nDELETE  {deleted.get('status', '?')}  uid={uid}")


if __name__ == "__main__":
    asyncio.run(main())
