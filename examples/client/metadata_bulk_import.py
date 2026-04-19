"""Bulk metadata import via /api/metadata — dry-run then real, with import params.

Mirrors upstream `example_4_data_element_create.py`. Shows the
`importStrategy`, `atomicMode`, `dryRun`, and `async` knobs on POST
/api/metadata — the single canonical entry for bulk-creating or
updating any mix of DHIS2 metadata in one atomic request.

Runs a DRY-RUN first so you see what DHIS2 would accept, then the real
import. Cleans up the two data elements it creates.

Usage:
    uv run python examples/client/metadata_bulk_import.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth, generate_uids
from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.enums import AggregationType, DataElementDomain, ValueType
from dhis2_client.generated.v42.schemas import DataElement


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


async def _default_category_combo(client: Dhis2Client) -> str:
    """Fetch the built-in default category combo UID via the typed accessor."""
    combos = await client.resources.category_combos.list(filters=["name:eq:default"], fields="id")
    return str(combos[0].id)


def _summary(response: dict[str, Any]) -> str:
    """Pretty-print the import counts from a /api/metadata response."""
    stats = (response.get("stats") or response.get("response", {}).get("stats")) or {}
    return json.dumps(stats, indent=2)


async def main() -> None:
    """Run a dry-run metadata import, then the real one, then clean up."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        uids = generate_uids(2)
        cc_uid = await _default_category_combo(client)
        print(f"minted: {uids}  default CC: {cc_uid}")

        # Each data element is a typed DataElement. `domainType`, `valueType`,
        # `aggregationType` are `StrEnum`s so typos fail at edit time.
        # The bulk envelope around them is a dict because /api/metadata has
        # no resource accessor — it accepts any mix of metadata types.
        data_elements = [
            DataElement(
                id=uid,
                code=f"EX_BULK_{uid}",
                name=f"Bulk example {idx + 1}",
                shortName=f"BulkEx{idx + 1}",
                domainType=DataElementDomain.AGGREGATE,
                valueType=ValueType.INTEGER_ZERO_OR_POSITIVE,
                aggregationType=AggregationType.SUM,
                categoryCombo=Reference(id=cc_uid),
            )
            for idx, uid in enumerate(uids)
        ]
        payload = {
            "dataElements": [de.model_dump(by_alias=True, exclude_none=True, mode="json") for de in data_elements],
        }

        # 1. DRY-RUN — DHIS2 validates the payload but persists nothing.
        print("\n>>> 1/3 dry-run via /api/metadata?importStrategy=CREATE_AND_UPDATE&atomicMode=ALL&dryRun=true")
        dry = await client.post_raw(
            "/api/metadata",
            payload,
            params={
                "importStrategy": "CREATE_AND_UPDATE",
                "atomicMode": "ALL",
                "dryRun": "true",
            },
        )
        print(_summary(dry))

        # 2. REAL IMPORT.
        print("\n>>> 2/3 real import")
        real = await client.post_raw(
            "/api/metadata",
            payload,
            params={
                "importStrategy": "CREATE_AND_UPDATE",
                "atomicMode": "ALL",
            },
        )
        print(_summary(real))

        # 3. CLEANUP — delete via the typed accessor.
        print("\n>>> 3/3 cleanup")
        for uid in uids:
            await client.resources.data_elements.delete(uid)
            print(f"    deleted dataElements/{uid}")


if __name__ == "__main__":
    asyncio.run(main())
