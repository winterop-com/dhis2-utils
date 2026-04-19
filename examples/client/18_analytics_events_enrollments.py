"""Event + enrollment analytics — `/api/analytics/events/query` and `/enrollments/query`.

Two analytics shapes distinct from the aggregate `/api/analytics` endpoint:

1. **Event analytics** (`/api/analytics/events/{query,aggregate}/{program}`) —
   line-listed events or grouped counts across a tracker/event program. Each
   row describes one event: psi, ps, eventdate, orgUnit, data-element values.
2. **Enrollment analytics** (`/api/analytics/enrollments/query/{program}`) —
   one row per tracker enrollment with its tracked-entity + attributes.

Both take the same dimension/filter DSL as `/api/analytics`:
`dx:<uid>`, `pe:LAST_12_MONTHS`, `ou:<uid>` (repeatable).

Uses the seeded Maternal Care program (`eke95YJi9VS`) from the e2e dump.
Falls back to a friendly message if the instance doesn't have tracker data.

Usage:
    uv run python examples/client/18_analytics_events_enrollments.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import os

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth

PROGRAM_UID = "eke95YJi9VS"  # Maternal Care — seeded tracker program with ANC + Delivery stages.
ORG_UNIT_UID = "NORNorway01"  # Norway root.


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
    """Run one event-query and one enrollment-query against the seeded tracker program."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        print(f"--- event analytics: program={PROGRAM_UID} ou={ORG_UNIT_UID} ---")
        events = await client.get_raw(
            f"/api/analytics/events/query/{PROGRAM_UID}",
            params={
                "dimension": [f"ou:{ORG_UNIT_UID}", "pe:LAST_12_MONTHS"],
                "outputType": "EVENT",
                "pageSize": 5,
                "skipMeta": "true",
            },
        )
        headers = [h["name"] for h in events.get("headers", [])]
        rows = events.get("rows", [])
        print(f"  headers ({len(headers)}): {headers[:6]}...")
        print(f"  rows: {len(rows)}")
        for row in rows[:3]:
            print(f"    {row[:6]}...")

        print(f"\n--- enrollment analytics: program={PROGRAM_UID} ---")
        enrollments = await client.get_raw(
            f"/api/analytics/enrollments/query/{PROGRAM_UID}",
            params={
                "dimension": [f"ou:{ORG_UNIT_UID}", "pe:LAST_12_MONTHS"],
                "pageSize": 5,
                "skipMeta": "true",
            },
        )
        headers = [h["name"] for h in enrollments.get("headers", [])]
        rows = enrollments.get("rows", [])
        print(f"  headers ({len(headers)}): {headers[:6]}...")
        print(f"  rows: {len(rows)}")
        for row in rows[:3]:
            print(f"    {row[:6]}...")


if __name__ == "__main__":
    asyncio.run(main())
