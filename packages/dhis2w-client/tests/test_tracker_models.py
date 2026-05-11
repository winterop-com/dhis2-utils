"""Unit tests for the tracker instance pydantic models."""

from __future__ import annotations

from dhis2w_client.generated.v42.tracker import (
    EnrollmentStatus,
    EventStatus,
    TrackerDataValue,
    TrackerEnrollment,
    TrackerEvent,
    TrackerTrackedEntity,
)


def test_event_status_enum_round_trips() -> None:
    """EventStatus is a StrEnum so it serialises to the same string DHIS2 uses."""
    assert EventStatus.COMPLETED == "COMPLETED"
    assert EventStatus("SCHEDULE") is EventStatus.SCHEDULE


def test_enrollment_status_enum_round_trips() -> None:
    """Enrollment status enum round trips."""
    assert EnrollmentStatus.ACTIVE == "ACTIVE"


def test_tracker_event_parses_typical_api_response() -> None:
    """Tracker event parses typical api response."""
    event = TrackerEvent.model_validate(
        {
            "event": "eventUid01",
            "program": "programUid1",
            "programStage": "stageUid001",
            "orgUnit": "orgUnitUid1",
            "status": "COMPLETED",
            "occurredAt": "2025-03-15T10:30:00.000",
            "dataValues": [
                {"dataElement": "deUid123456", "value": "42"},
                {"dataElement": "deUid789012", "value": "high"},
            ],
        }
    )
    assert event.event == "eventUid01"
    assert event.status is EventStatus.COMPLETED
    assert event.dataValues is not None
    assert len(event.dataValues) == 2
    assert event.dataValues[0].value == "42"


def test_tracker_enrollment_with_nested_events() -> None:
    """Tracker enrollment with nested events."""
    enrollment = TrackerEnrollment.model_validate(
        {
            "enrollment": "enr01234567",
            "trackedEntity": "te012345678",
            "program": "pr012345678",
            "orgUnit": "ou012345678",
            "status": "ACTIVE",
            "events": [
                {"event": "ev012345678", "status": "COMPLETED"},
            ],
        }
    )
    assert enrollment.status is EnrollmentStatus.ACTIVE
    assert enrollment.events is not None
    assert len(enrollment.events) == 1
    assert enrollment.events[0].status is EventStatus.COMPLETED


def test_tracker_tracked_entity_preserves_attributes_and_type_ref() -> None:
    """TrackedEntityType is carried as a UID string reference — the full metadata lives at
    /api/trackedEntityTypes/{uid}. Consumers can join the two via `client.resources.tracked_entity_types.get()`.
    """
    entity = TrackerTrackedEntity.model_validate(
        {
            "trackedEntity": "te012345678",
            "trackedEntityType": "tet01234567",
            "orgUnit": "ou012345678",
            "attributes": [
                {"attribute": "attr1234567", "value": "Alice", "valueType": "TEXT"},
                {"attribute": "attr7654321", "value": "1985-04-12", "valueType": "DATE"},
            ],
        }
    )
    assert entity.trackedEntity == "te012345678"
    assert entity.trackedEntityType == "tet01234567"
    assert entity.attributes is not None
    assert len(entity.attributes) == 2
    assert entity.attributes[0].value == "Alice"


def test_data_value_parses_event_payload() -> None:
    """Data value parses event payload."""
    dv = TrackerDataValue.model_validate({"dataElement": "de012345678", "value": "10"})
    assert dv.dataElement == "de012345678"
    assert dv.value == "10"


def test_extra_fields_are_preserved_on_tracker_models() -> None:
    """`extra='allow'` — new DHIS2 fields flow through without breaking callers."""
    event = TrackerEvent.model_validate({"event": "ev012345678", "futureField": "some-value", "status": "ACTIVE"})
    dumped = event.model_dump(exclude_none=True)
    assert dumped["futureField"] == "some-value"
