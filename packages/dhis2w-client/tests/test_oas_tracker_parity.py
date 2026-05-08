"""Parity tests: OAS-derived tracker models parse a real DHIS2 response.

Fixture captured from the seeded e2e dump via
`GET /api/tracker/trackedEntities?trackedEntityType=FsgEX4d3Fc5&fields=*`.
Pins the wire shape so a regen that silently drops a field fails the test
instead of surfacing as a runtime KeyError months later.
"""

from __future__ import annotations

import json
from pathlib import Path

from dhis2w_client.generated.v42.tracker import (
    EnrollmentStatus,
    EventStatus,
    TrackerTrackedEntity,
)

_FIXTURE = Path(__file__).parent / "fixtures" / "openapi_parity" / "tracker_tracked_entities.json"


def test_real_tracked_entity_parses_cleanly() -> None:
    """OAS-derived TrackerTrackedEntity round-trips a real /api/tracker response."""
    payload = json.loads(_FIXTURE.read_text())
    entities = [TrackerTrackedEntity.model_validate(raw) for raw in payload["trackedEntities"]]
    assert len(entities) >= 1
    first = entities[0]
    assert first.trackedEntity is not None
    assert first.trackedEntityType is not None
    assert first.orgUnit is not None
    assert first.attributes is not None
    assert first.enrollments is not None
    # Every enrollment's status round-trips through the generated StrEnum.
    for enrollment in first.enrollments:
        assert enrollment.status is None or isinstance(enrollment.status, EnrollmentStatus)
        if enrollment.events:
            for event in enrollment.events:
                assert event.status is None or isinstance(event.status, EventStatus)


def test_tracker_entity_round_trip_dump_matches_input_keys() -> None:
    """Dumping the parsed model re-produces the core wire keys without drift."""
    payload = json.loads(_FIXTURE.read_text())
    raw = payload["trackedEntities"][0]
    parsed = TrackerTrackedEntity.model_validate(raw)
    dumped = parsed.model_dump(by_alias=True, exclude_none=True, mode="json")
    # The subset of keys we promise stability on.
    for stable_key in ("trackedEntity", "trackedEntityType", "orgUnit"):
        if stable_key in raw:
            assert dumped[stable_key] == raw[stable_key], f"{stable_key} drifted on round-trip"
