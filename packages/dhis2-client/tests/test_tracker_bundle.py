"""Unit tests for TrackerBundle — the typed /api/tracker write payload."""

from __future__ import annotations

from datetime import datetime

from dhis2_client import EventStatus, TrackerBundle, TrackerEnrollment, TrackerEvent, TrackerTrackedEntity


def test_empty_bundle_serialises_to_empty_arrays() -> None:
    """Default `TrackerBundle()` produces a payload with empty arrays, not missing keys."""
    bundle = TrackerBundle()
    payload = bundle.model_dump(by_alias=True, exclude_none=True, mode="json")
    # No explicit trackedEntities/enrollments/events/relationships yet — exclude_none drops them
    assert payload == {
        "trackedEntities": [],
        "enrollments": [],
        "events": [],
        "relationships": [],
    }


def test_nested_construction_matches_dhis2_wire_shape() -> None:
    """Nested construction (TrackedEntity > Enrollments > Events) matches the /api/tracker wire format."""
    bundle = TrackerBundle(
        trackedEntities=[
            TrackerTrackedEntity(
                trackedEntityType="tetXXXXXXX1",
                orgUnit="ouXXXXXXXXX",
                enrollments=[
                    TrackerEnrollment(
                        program="progXXXXXXX",
                        orgUnit="ouXXXXXXXXX",
                        enrolledAt=datetime(2026, 1, 1),
                        occurredAt=datetime(2026, 1, 1),
                        events=[
                            TrackerEvent(
                                program="progXXXXXXX",
                                orgUnit="ouXXXXXXXXX",
                                status=EventStatus.COMPLETED,
                                occurredAt=datetime(2026, 1, 1),
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
    payload = bundle.model_dump(by_alias=True, exclude_none=True, mode="json")
    te = payload["trackedEntities"][0]
    assert te["trackedEntityType"] == "tetXXXXXXX1"
    assert te["orgUnit"] == "ouXXXXXXXXX"
    enr = te["enrollments"][0]
    assert enr["program"] == "progXXXXXXX"
    ev = enr["events"][0]
    assert ev["status"] == "COMPLETED"  # StrEnum -> wire string
    assert ev["occurredAt"] == "2026-01-01T00:00:00"


def test_flat_construction_independent_arrays() -> None:
    """Flat construction — all four top-level arrays can be populated independently."""
    bundle = TrackerBundle(
        events=[
            TrackerEvent(
                event="evtXXXXXXX1",  # existing event UID to update
                status=EventStatus.COMPLETED,
            ),
            TrackerEvent(
                event="evtXXXXXXX2",
                status=EventStatus.SKIPPED,
            ),
        ],
    )
    payload = bundle.model_dump(by_alias=True, exclude_none=True, mode="json")
    assert len(payload["events"]) == 2
    assert payload["events"][0]["status"] == "COMPLETED"
    assert payload["events"][1]["status"] == "SKIPPED"
    assert payload["trackedEntities"] == []


def test_extra_fields_preserved_on_write_payload() -> None:
    """`extra='allow'` lets callers pass fields DHIS2 introduces in later versions."""
    bundle = TrackerBundle.model_validate(
        {
            "events": [{"event": "ev1", "status": "COMPLETED", "futureField": "some-new-value"}],
        }
    )
    payload = bundle.model_dump(by_alias=True, exclude_none=True, mode="json")
    assert payload["events"][0]["futureField"] == "some-new-value"


def test_exported_from_top_level() -> None:
    import dhis2_client

    assert dhis2_client.TrackerBundle is TrackerBundle
