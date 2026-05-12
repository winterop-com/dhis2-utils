"""Bulk dataValueSets push grouped by dataset — forward-compat across v41/v42/v43.

Demonstrates `client.data_values.import_grouped_by_dataset(values, ...)`
— required on v43 for any DataElement that belongs to multiple
DataSets (BUGS.md #35). v41/v42 also accept the explicit envelope
shape, so callers can write the same code on all three majors.

On v43 this is necessary: bare `/api/dataValueSets` POSTs that mix
values whose DEs belong to multiple DataSets get rejected with
`409 E8002 Data set detection failed` (BUGS.md #35). v41 + v42
silently auto-target one of the matching DataSets, but they ALSO
accept the explicit envelope — so this code path works unchanged
when the target upgrades.

This file lives in `examples/v43/client/` and runs against a v41
stack; identical code lives in `examples/v42/client/` and
`examples/v43/client/` (only the version-pinned `dhis2w_client.v{N}`
import differs).

Usage:
    uv run python examples/v43/client/aggregate_bulk_grouped.py

Requires: a stack with at least one DataSet that has both
DataElements + OrganisationUnits attached (the seeded Sierra Leone
fixture qualifies).
"""

from __future__ import annotations

from _runner import run_example
from dhis2w_client.v43 import DataValue
from dhis2w_core.profile import profile_from_env
from dhis2w_core.v43.client_context import open_client


async def main() -> None:
    """Build 3 typed DataValues and push them grouped by DataSet (v43 — necessary, not optional)."""
    async with open_client(profile_from_env()) as client:
        # Find a seeded DataSet with DEs + OUs to write against.
        envelope = await client.get_raw(
            "/api/dataSets",
            params={
                "fields": "id,periodType,dataSetElements[dataElement[id]],organisationUnits[id]",
                "filter": ["dataSetElements:!empty", "organisationUnits:!empty"],
                "pageSize": "1",
            },
        )
        ds_rows = envelope.get("dataSets") or []
        if not ds_rows:
            print("no DataSet with DEs + OUs — skipping bulk demo")
            return
        ds = ds_rows[0]
        de_uid = ((ds.get("dataSetElements") or [{}])[0].get("dataElement") or {}).get("id")
        ou_uid = (ds.get("organisationUnits") or [{}])[0].get("id")
        period = "210701" if ds.get("periodType") == "Monthly" else "2107"

        # Build typed DataValues — same shape across v41/v42/v43.
        values = [
            DataValue(
                dataElement=de_uid,
                period=period,
                orgUnit=ou_uid,
                categoryOptionCombo="HllvX50cXC0",
                attributeOptionCombo="HllvX50cXC0",
                value=str(n),
            )
            for n in (10, 20, 30)
        ]

        # The grouped push pre-fetches DE→DataSet membership and chunks
        # by DataSet. Works on v41 + v42 + v43.
        responses = await client.data_values.import_grouped_by_dataset(values, chunk_size=10, force=True)
        for i, resp in enumerate(responses):
            count = resp.import_count()
            if count is not None:
                print(f"  chunk {i}: imported={count.imported} updated={count.updated} ignored={count.ignored}")
            else:
                print(f"  chunk {i}: {resp.status} (no import_count in envelope)")


if __name__ == "__main__":
    run_example(main)
