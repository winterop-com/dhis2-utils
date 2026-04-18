"""Analytics queries and resource-table refresh.

Two things:
  1. Query `/api/analytics` for a few DHIS2 indicators over a time range.
  2. Trigger `/api/resourceTables/analytics` so DHIS2 re-populates the
     analytics_* tables after fresh data has been pushed.

The refresh returns a task id; the official docker stack runs an
`analytics-trigger` sidecar that polls to completion — for a one-shot
dev check you can `docker restart analytics-trigger` and `docker wait`.

Usage:
    uv run python examples/07_analytics.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import json
import os

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


async def main() -> None:
    """Run an aggregated analytics query, then trigger a refresh."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        # ANC 1st visit across all 4 Norway fylker for the last 12 months.
        # dx = data element / indicator, pe = period, ou = org unit.
        analytics = await client.get_raw(
            "/api/analytics",
            params={
                "dimension": [
                    "dx:DEancVisit1;DEancVisit4",
                    "pe:LAST_12_MONTHS",
                    "ou:NORNorway01;LEVEL-2",
                ],
                "skipMeta": "true",
            },
        )
        rows = analytics.get("rows", [])
        print(f"analytics rows: {len(rows)} (header: {analytics.get('headers', [])[:4]})")
        for row in rows[:10]:
            print("  ", row)

        # Trigger analytics-table refresh. Returns a task id; analytics-trigger
        # sidecar polls it; for your own polling see /api/system/tasks/ANALYTICS_TABLE/<id>.
        trigger = await client.post_raw("/api/resourceTables/analytics")
        task_id = (trigger.get("response") or {}).get("id")
        print(f"analytics refresh queued (task={task_id}).")
        print(json.dumps(trigger, indent=2)[:400])


if __name__ == "__main__":
    asyncio.run(main())
