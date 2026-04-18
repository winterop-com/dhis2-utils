"""Bulk metadata import via /api/metadata — dry-run then real, with import params.

Mirrors upstream `example_4_data_element_create.py`. Shows the
`importStrategy`, `atomicMode`, `dryRun`, and `async` knobs on POST
/api/metadata — the single canonical entry for bulk-creating or
updating any mix of DHIS2 metadata in one atomic request.

Runs a DRY-RUN first so you see what DHIS2 would accept, then the real
import. Cleans up the two data elements it creates.

Usage:
    uv run python examples/client/10_metadata_bulk_import.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


async def _mint_uids(client: Dhis2Client, count: int) -> list[str]:
    """Ask DHIS2 for `count` fresh UIDs."""
    response = await client.get_raw("/api/system/id", params={"limit": count})
    return [str(c) for c in response["codes"]]


async def _default_category_combo(client: Dhis2Client) -> str:
    """Fetch the built-in default category combo UID."""
    response = await client.get_raw(
        "/api/categoryCombos",
        params={"filter": "name:eq:default", "fields": "id"},
    )
    return str(response["categoryCombos"][0]["id"])


def _summary(response: dict[str, Any]) -> str:
    """Pretty-print the import counts from a /api/metadata response."""
    stats = (response.get("stats") or response.get("response", {}).get("stats")) or {}
    return json.dumps(stats, indent=2)


async def main() -> None:
    """Run a dry-run metadata import, then the real one, then clean up."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        uids = await _mint_uids(client, 2)
        cc_uid = await _default_category_combo(client)
        print(f"minted: {uids}  default CC: {cc_uid}")

        payload = {
            "dataElements": [
                {
                    "id": uid,
                    "code": f"EX_BULK_{uid}",
                    "name": f"Bulk example {idx + 1}",
                    "shortName": f"BulkEx{idx + 1}",
                    "domainType": "AGGREGATE",
                    "valueType": "INTEGER_ZERO_OR_POSITIVE",
                    "aggregationType": "SUM",
                    "categoryCombo": {"id": cc_uid},
                }
                for idx, uid in enumerate(uids)
            ]
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

        # 3. CLEANUP — delete both.
        print("\n>>> 3/3 cleanup")
        for uid in uids:
            await client.delete_raw(f"/api/dataElements/{uid}")
            print(f"    deleted /api/dataElements/{uid}")


if __name__ == "__main__":
    asyncio.run(main())
