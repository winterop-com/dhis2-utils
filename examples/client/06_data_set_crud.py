"""Full CRUD lifecycle for a data set — create, assign members, read, update, delete.

Shows the assignment dance DHIS2 requires for data sets: you need to
create the data set *and* attach a list of data-set-elements referencing
existing data elements *and* a list of organisation-unit assignments in
the same POST, or you end up with an empty dataset nothing can write to.

Uses UIDs from the seeded Norway fixture (DEancVisit1, NOROsloProv, etc)
so the created dataset has something meaningful to reference. Cleans up
even on failure via a try/finally.

Usage:
    uv run python examples/06_data_set_crud.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import os

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth
from dhis2_client.generated.v42.schemas.data_set import DataSet, Reference

# Seeded UIDs from infra/dhis.sql.gz — see docs/local-setup.md.
DATA_ELEMENT_UIDS = ["DEancVisit1", "DEancVisit4", "DEdelFacilt"]
ORG_UNIT_UIDS = ["NOROsloProv", "NORVestland"]


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
    """Ask DHIS2 for a fresh server-generated UID (utility endpoint, not a resource)."""
    response = await client.get_raw("/api/system/id", params={"limit": 1})
    return str(response["codes"][0])


async def _default_category_combo(client: Dhis2Client) -> str:
    """Fetch the built-in default category combo UID via the typed accessor."""
    combos = await client.resources.category_combos.list(filters=["name:eq:default"], fields="id")
    return str(combos[0].id)


async def main() -> None:
    """Walk a data set through its full lifecycle."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        uid = await _mint_uid(client)
        print(f"minted UID: {uid}")
        category_combo_uid = await _default_category_combo(client)

        new_dataset = DataSet(
            id=uid,
            code=f"EX_DS_{uid}",
            name=f"Example monthly dataset {uid}",
            shortName=f"Ex DS {uid[:6]}",
            periodType="Monthly",
            categoryCombo=Reference(id=category_combo_uid),
            # DataSetElement has no typed schema in the generator (list[Any]).
            dataSetElements=[{"dataElement": {"id": de_uid}, "dataSet": {"id": uid}} for de_uid in DATA_ELEMENT_UIDS],
            organisationUnits=[Reference(id=ou_uid) for ou_uid in ORG_UNIT_UIDS],
            openFuturePeriods=0,
            timelyDays=15,
        )
        created = await client.resources.data_sets.create(new_dataset)
        print(f"\nCREATE  {created.get('status', '?')}  uid={uid}")

        try:
            fetched = await client.resources.data_sets.get(
                uid,
                fields=(
                    "id,code,name,periodType,timelyDays,"
                    "dataSetElements[dataElement[id,name]],"
                    "organisationUnits[id,name]"
                ),
            )
            print(
                f"READ    id={fetched.id}  periodType={fetched.periodType}  "
                f"elements={len(fetched.dataSetElements or [])}  orgunits={len(fetched.organisationUnits or [])}"
            )

            # JSON Patch for partial update — no typed accessor today; raw by design.
            await client.patch_raw(
                f"/api/dataSets/{uid}",
                [{"op": "replace", "path": "/timelyDays", "value": 30}],
            )
            updated = await client.resources.data_sets.get(uid, fields="id,name,timelyDays,lastUpdated")
            print(f"PATCH   timelyDays={updated.timelyDays}  lastUpdated={updated.lastUpdated}")
        finally:
            deleted = await client.resources.data_sets.delete(uid)
            print(f"\nDELETE  {deleted.get('status', '?')}  uid={uid}")


if __name__ == "__main__":
    asyncio.run(main())
