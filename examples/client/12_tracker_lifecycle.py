"""Tracker lifecycle — create a tracked entity with an enrollment + event.

Shows the `/api/tracker` write path: one atomic POST creates a tracked entity,
its enrollment in a program, and the first event against that enrollment.
Then reads it back via the typed `TrackerTrackedEntity` / `TrackerEnrollment`
/ `TrackerEvent` models.

The seeded e2e fixture has no tracker programs, so this script targets
`play.dhis2.org/dev` by default. Override with `DHIS2_URL` + credentials.

Usage:
    uv run python examples/client/12_tracker_lifecycle.py

Env:
    DHIS2_URL     base URL (default: https://play.im.dhis2.org/dev)
    DHIS2_PAT     OR DHIS2_USERNAME + DHIS2_PASSWORD
    PROGRAM_UID   tracker program UID to enroll against
    ORG_UNIT_UID  OU UID that's in admin's capture scope
    TET_UID       TrackedEntityType UID (e.g. Person)
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime

from dhis2_client import AuthProvider, BasicAuth, Dhis2Client, EventStatus, PatAuth, WebMessageResponse


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
    """Create a tracked-entity bundle, read it back, soft-delete."""
    base_url = os.environ.get("DHIS2_URL", "https://play.im.dhis2.org/dev")
    program_uid = os.environ.get("PROGRAM_UID")
    ou_uid = os.environ.get("ORG_UNIT_UID")
    tet_uid = os.environ.get("TET_UID")
    if not (program_uid and ou_uid and tet_uid):
        print("set PROGRAM_UID, ORG_UNIT_UID, TET_UID — this script needs a tracker-populated instance")
        return

    bundle = {
        "trackedEntities": [
            {
                "trackedEntityType": tet_uid,
                "orgUnit": ou_uid,
                "enrollments": [
                    {
                        "program": program_uid,
                        "orgUnit": ou_uid,
                        "enrolledAt": datetime.now().isoformat(timespec="seconds"),
                        "occurredAt": datetime.now().isoformat(timespec="seconds"),
                        "events": [
                            {
                                "program": program_uid,
                                "orgUnit": ou_uid,
                                "status": EventStatus.COMPLETED,
                                "occurredAt": datetime.now().isoformat(timespec="seconds"),
                            },
                        ],
                    },
                ],
            },
        ],
    }

    async with Dhis2Client(base_url, auth=_auth_from_env()) as client:
        print("POST /api/tracker (importStrategy=CREATE_AND_UPDATE)")
        raw = await client.post_raw(
            "/api/tracker",
            bundle,
            params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL"},
        )
        response = WebMessageResponse.model_validate(raw)
        print(f"  status={response.status}  message={response.message}")
        counts = response.import_count()
        if counts is not None:
            print(f"  imported={counts.imported} updated={counts.updated} ignored={counts.ignored}")
        for conflict in response.conflicts()[:5]:
            print(f"  conflict: {conflict.property} = {conflict.value} [{conflict.errorCode}]")

        # Read the full tracked-entity population for the program.
        raw_read = await client.get_raw(
            "/api/tracker/trackedEntities",
            params={
                "program": program_uid,
                "pageSize": 3,
                "fields": "trackedEntity,trackedEntityType,orgUnit,enrollments",
            },
        )
        entities = raw_read.get("instances", [])
        print(f"\ntracked entities in program {program_uid}: {len(entities)}")
        for entity in entities[:3]:
            print(f"  uid={entity.get('trackedEntity')}  type={entity.get('trackedEntityType')}")


if __name__ == "__main__":
    asyncio.run(main())
