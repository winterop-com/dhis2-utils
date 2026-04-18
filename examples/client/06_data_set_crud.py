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
import json
import os
from typing import Any

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth

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
    """Ask DHIS2 for a fresh server-generated UID."""
    response = await client.get_raw("/api/system/id", params={"limit": 1})
    codes = response.get("codes", [])
    return str(codes[0])


async def _dump(label: str, payload: Any) -> None:
    """Print a labelled JSON block, truncated."""
    print(f"\n=== {label} ===")
    print(json.dumps(payload, indent=2)[:900])


async def _default_category_combo(client: Dhis2Client) -> str:
    """Fetch the built-in default category combo UID."""
    response = await client.get_raw(
        "/api/categoryCombos",
        params={"filter": "name:eq:default", "fields": "id"},
    )
    return str(response["categoryCombos"][0]["id"])


async def main() -> None:
    """Walk a data set through its full lifecycle."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), pin_version=Dhis2.V42) as client:
        uid = await _mint_uid(client)
        print(f"minted UID: {uid}")
        category_combo_uid = await _default_category_combo(client)

        # CREATE — dataset + data-set-elements + org-unit assignments, all in one POST.
        new_dataset = {
            "id": uid,
            "code": f"EX_DS_{uid}",
            "name": f"Example monthly dataset {uid}",
            "shortName": f"Ex DS {uid[:6]}",
            "periodType": "Monthly",
            "categoryCombo": {"id": category_combo_uid},
            "dataSetElements": [
                {"dataElement": {"id": de_uid}, "dataSet": {"id": uid}} for de_uid in DATA_ELEMENT_UIDS
            ],
            "organisationUnits": [{"id": ou_uid} for ou_uid in ORG_UNIT_UIDS],
            "openFuturePeriods": 0,
            "timelyDays": 15,
        }
        created = await client.post_raw("/api/dataSets", new_dataset)
        await _dump("CREATE /api/dataSets", created.get("response", created))

        try:
            # READ — pull the dataset back with expanded assignments.
            fetched = await client.get_raw(
                f"/api/dataSets/{uid}",
                params={
                    "fields": (
                        "id,code,name,periodType,timelyDays,"
                        "dataSetElements[dataElement[id,name]],"
                        "organisationUnits[id,name]"
                    ),
                },
            )
            await _dump(f"READ /api/dataSets/{uid}", fetched)

            # UPDATE — bump timelyDays via JSON Patch.
            await client.patch_raw(
                f"/api/dataSets/{uid}",
                [{"op": "replace", "path": "/timelyDays", "value": 30}],
            )
            updated = await client.get_raw(
                f"/api/dataSets/{uid}",
                params={"fields": "id,name,timelyDays,lastUpdated"},
            )
            await _dump(f"PATCH /api/dataSets/{uid}", updated)

        finally:
            # DELETE — always, so reruns start clean.
            deleted = await client.delete_raw(f"/api/dataSets/{uid}")
            await _dump(f"DELETE /api/dataSets/{uid}", deleted)


if __name__ == "__main__":
    asyncio.run(main())
