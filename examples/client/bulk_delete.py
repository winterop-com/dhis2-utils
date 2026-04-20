"""Tear down metadata in one call — `client.metadata.delete_bulk`.

Wraps `POST /api/metadata?importStrategy=DELETE` with a minimal
`{resource_type: [{id: uid}, ...]}` bundle, so one HTTP request deletes
every UID at once. Useful for:

- Fixture teardown after a test run.
- Reacting to a `dhis2 doctor` report — feed it a list of orphan UIDs
  the probes surfaced.
- Bulk cleanup after a scripted import that's obsolete.

Two entry points:

- `client.metadata.delete_bulk(resource_type, uids)` — single resource
  type, single HTTP call.
- `client.metadata.delete_bulk_multi({resource: [uids], ...})` — cross
  multiple resource types in one bundle. `atomic_mode="ALL"` rolls the
  whole bundle back on any conflict; the default `"NONE"` lets partial
  failures through (typical deletion usage).

Usage:
    uv run python examples/client/bulk_delete.py
"""

from __future__ import annotations

from _runner import run_example
from dhis2_client import generate_uid
from dhis2_core.client_context import open_client
from dhis2_core.profile import profile_from_env


async def main() -> None:
    """Create three throwaway DataElements, bulk-delete them, show the import-report stats."""
    async with open_client(profile_from_env()) as client:
        default_cc = await client.system.default_category_combo_uid()
        uids = [generate_uid() for _ in range(3)]
        print(f"creating 3 test DataElements: {uids}")
        for uid in uids:
            await client.post_raw(
                "/api/dataElements",
                body={
                    "id": uid,
                    "name": f"bulk-delete-demo {uid}",
                    "shortName": f"bdd-{uid[:7]}",
                    "aggregationType": "SUM",
                    "domainType": "AGGREGATE",
                    "valueType": "TEXT",
                    "categoryCombo": {"id": default_cc},
                },
            )

        before = await client.get_raw(
            "/api/dataElements",
            params={"filter": "name:like:bulk-delete-demo", "fields": "id"},
        )
        print(f"before delete: {len(before.get('dataElements', []))} matching")

        # One HTTP call deletes every UID.
        envelope = await client.metadata.delete_bulk("dataElements", uids)
        report = envelope.import_report()
        stats = report.stats if report else None
        print(f"delete_bulk -> import_report.stats.deleted = {stats.deleted if stats else '?'}")

        after = await client.get_raw(
            "/api/dataElements",
            params={"filter": "name:like:bulk-delete-demo", "fields": "id"},
        )
        print(f"after delete: {len(after.get('dataElements', []))} matching")

        # Empty list short-circuits — no HTTP call.
        print("\nempty-input short-circuit:")
        noop = await client.metadata.delete_bulk("dataElements", [])
        print(f"  status={noop.status}  message={noop.message}")

        # `delete_bulk_multi` for cross-type teardown. (Nothing to delete
        # here — just shows the shape for a real cleanup script.)
        print("\ndelete_bulk_multi — multi-type shape:")
        multi = await client.metadata.delete_bulk_multi(
            {
                "dataElements": [],
                "indicators": [],
            }
        )
        print(f"  status={multi.status}  message={multi.message}")


if __name__ == "__main__":
    run_example(main)
