"""Tracker lifecycle — create a tracked entity with an enrollment + event.

Shows the `/api/tracker` write path: one atomic POST creates a tracked entity,
its enrollment in a program, and the first event against that enrollment.
Then reads it back via the typed `TrackerTrackedEntity` / `TrackerEnrollment`
/ `TrackerEvent` models.

The seeded e2e fixture has no tracker programs, so this script targets
`play.dhis2.org/dev` by default. Override with `DHIS2_URL` + credentials.

Usage:
    uv run python examples/client/tracker_lifecycle.py

Env:
    DHIS2_URL     base URL (default: https://play.im.dhis2.org/dev)
    DHIS2_PAT     OR DHIS2_USERNAME + DHIS2_PASSWORD
    PROGRAM_UID   tracker program UID to enroll against
    ORG_UNIT_UID  OU UID that's in admin's capture scope
    TET_UID       TrackedEntityType UID (e.g. Person)
"""

from __future__ import annotations

import os
from datetime import datetime

from _runner import run_example
from dhis2_client import WebMessageResponse
from dhis2_client.generated.v42.tracker import (
    EnrollmentStatus,
    EventStatus,
    TrackerBundle,
    TrackerEnrollment,
    TrackerEvent,
    TrackerTrackedEntity,
)
from dhis2_core.client_context import open_client
from dhis2_core.profile import profile_from_env


async def main() -> None:
    """Create a tracked-entity bundle, read it back, soft-delete."""
    program_uid = os.environ.get("PROGRAM_UID")
    ou_uid = os.environ.get("ORG_UNIT_UID")
    tet_uid = os.environ.get("TET_UID")
    if not (program_uid and ou_uid and tet_uid):
        print("set PROGRAM_UID, ORG_UNIT_UID, TET_UID — this script needs a tracker-populated instance")
        return

    now = datetime.now()
    bundle = TrackerBundle(
        trackedEntities=[
            TrackerTrackedEntity(
                trackedEntityType=tet_uid,
                orgUnit=ou_uid,
                enrollments=[
                    TrackerEnrollment(
                        program=program_uid,
                        orgUnit=ou_uid,
                        status=EnrollmentStatus.ACTIVE,
                        enrolledAt=now,
                        occurredAt=now,
                        events=[
                            TrackerEvent(
                                program=program_uid,
                                orgUnit=ou_uid,
                                status=EventStatus.COMPLETED,
                                occurredAt=now,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    async with open_client(profile_from_env()) as client:
        print("POST /api/tracker (importStrategy=CREATE_AND_UPDATE)")
        raw = await client.post_raw(
            "/api/tracker",
            bundle.model_dump(by_alias=True, exclude_none=True, mode="json"),
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
    run_example(main)
