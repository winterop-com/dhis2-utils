"""Typed models for DHIS2 v42 tracker instance data.

Lives under `generated/v42/` alongside the codegen-emitted metadata schemas
because the tracker shape at `/api/tracker/*` drifts across DHIS2 majors
(field additions / renames / removals between v42 and later versions).
Pinning these models to v42 means a v43 bump can ship its own
`generated/v43/tracker.py` without touching v42 callers.

Hand-written (not codegen-emitted) because `/api/schemas` doesn't describe
tracker *instance* shapes — those only appear in the OpenAPI spec. Regen
of this version directory leaves this file alone; the codegen template
only writes `schemas/`, `resources.py`, `common.py`, `enums.py`, and the
version `__init__.py`.

Models here cover the cases our service layer touches:

| DHIS2 schema         | Class                    | Endpoint                              |
|----------------------|--------------------------|----------------------------------------|
| TrackerTrackedEntity | `TrackerTrackedEntity`   | `/api/tracker/trackedEntities`        |
| TrackerEnrollment    | `TrackerEnrollment`      | `/api/tracker/enrollments`            |
| TrackerEvent         | `TrackerEvent`           | `/api/tracker/events`                 |
| RelationshipItem     | `TrackerRelationship`    | `/api/tracker/relationships`          |

Status enums (`EnrollmentStatus`, `EventStatus`) are the exact values DHIS2
v42 uses on the wire; `StrEnum` keeps them round-trippable through JSON.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EnrollmentStatus(StrEnum):
    """Tracker enrollment status — ACTIVE is the normal case; COMPLETED/CANCELLED are terminal."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class EventStatus(StrEnum):
    """Tracker event status — the full set DHIS2 accepts on write + emits on read."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    VISITED = "VISITED"
    SCHEDULE = "SCHEDULE"
    OVERDUE = "OVERDUE"
    SKIPPED = "SKIPPED"


class TrackerAttributeValue(BaseModel):
    """One tracked-entity attribute value on a TrackerTrackedEntity / TrackerEvent payload."""

    model_config = ConfigDict(extra="allow")

    attribute: str | None = None
    value: str | None = None
    displayName: str | None = None
    valueType: str | None = None
    storedBy: str | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class TrackerDataValue(BaseModel):
    """One data-element value captured on a TrackerEvent."""

    model_config = ConfigDict(extra="allow")

    dataElement: str | None = None
    value: str | None = None
    providedElsewhere: bool | None = None
    storedBy: str | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


class TrackerNote(BaseModel):
    """One note attached to an enrollment or event."""

    model_config = ConfigDict(extra="allow")

    note: str | None = None
    value: str | None = None
    storedBy: str | None = None
    storedAt: datetime | None = None


class TrackerEvent(BaseModel):
    """One tracker event (`/api/tracker/events`)."""

    model_config = ConfigDict(extra="allow")

    event: str | None = None
    trackedEntity: str | None = None
    enrollment: str | None = None
    program: str | None = None
    programStage: str | None = None
    orgUnit: str | None = None
    status: EventStatus | None = None
    occurredAt: datetime | None = None
    scheduledAt: datetime | None = None
    completedAt: datetime | None = None
    completedBy: str | None = None
    followUp: bool | None = None
    deleted: bool | None = None
    attributeOptionCombo: str | None = None
    attributeCategoryOptions: str | None = None
    assignedUser: str | None = None
    storedBy: str | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    dataValues: list[TrackerDataValue] = Field(default_factory=list)
    notes: list[TrackerNote] = Field(default_factory=list)
    relationships: list[Any] = Field(default_factory=list)
    geometry: dict[str, Any] | None = None


class TrackerEnrollment(BaseModel):
    """One tracker enrollment (`/api/tracker/enrollments`)."""

    model_config = ConfigDict(extra="allow")

    enrollment: str | None = None
    trackedEntity: str | None = None
    program: str | None = None
    orgUnit: str | None = None
    status: EnrollmentStatus | None = None
    enrolledAt: datetime | None = None
    occurredAt: datetime | None = None
    completedAt: datetime | None = None
    completedBy: str | None = None
    followUp: bool | None = None
    deleted: bool | None = None
    storedBy: str | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    attributes: list[TrackerAttributeValue] = Field(default_factory=list)
    events: list[TrackerEvent] = Field(default_factory=list)
    notes: list[TrackerNote] = Field(default_factory=list)
    relationships: list[Any] = Field(default_factory=list)
    geometry: dict[str, Any] | None = None


class TrackerTrackedEntity(BaseModel):
    """One tracked entity (`/api/tracker/trackedEntities`)."""

    model_config = ConfigDict(extra="allow")

    trackedEntity: str | None = None
    trackedEntityType: str | None = None
    orgUnit: str | None = None
    inactive: bool | None = None
    deleted: bool | None = None
    potentialDuplicate: bool | None = None
    storedBy: str | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    attributes: list[TrackerAttributeValue] = Field(default_factory=list)
    enrollments: list[TrackerEnrollment] = Field(default_factory=list)
    relationships: list[Any] = Field(default_factory=list)
    programOwners: list[Any] = Field(default_factory=list)
    geometry: dict[str, Any] | None = None


class TrackerRelationshipItem(BaseModel):
    """One side of a tracker relationship (`from` or `to`)."""

    model_config = ConfigDict(extra="allow")

    trackedEntity: dict[str, Any] | None = None
    enrollment: dict[str, Any] | None = None
    event: dict[str, Any] | None = None


class TrackerRelationship(BaseModel):
    """One tracker relationship (`/api/tracker/relationships`)."""

    model_config = ConfigDict(extra="allow")

    relationship: str | None = None
    relationshipType: str | None = None
    bidirectional: bool | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    from_: TrackerRelationshipItem | None = Field(default=None, alias="from")
    to: TrackerRelationshipItem | None = None


class TrackerBundle(BaseModel):
    """Typed payload for `POST /api/tracker` — any mix of tracker objects in one atomic write.

    DHIS2 accepts nested construction (a tracked entity carrying its own
    `enrollments[]` which carry their own `events[]`) or flat construction
    (all four arrays populated independently). Callers pick whichever fits
    their data shape; DHIS2 collapses both forms server-side.

    Produce the wire payload with
    `bundle.model_dump(by_alias=True, exclude_none=True, mode="json")`.
    The `trackedEntities` / `enrollments` / `events` / `relationships` arrays
    are each typed lists of the existing tracker models, so enum fields like
    `EventStatus.COMPLETED` and nested attributes / data values are validated
    at construction time.
    """

    model_config = ConfigDict(extra="allow")

    trackedEntities: list[TrackerTrackedEntity] = Field(default_factory=list)
    enrollments: list[TrackerEnrollment] = Field(default_factory=list)
    events: list[TrackerEvent] = Field(default_factory=list)
    relationships: list[TrackerRelationship] = Field(default_factory=list)


__all__ = [
    "EnrollmentStatus",
    "EventStatus",
    "TrackerAttributeValue",
    "TrackerBundle",
    "TrackerDataValue",
    "TrackerEnrollment",
    "TrackerEvent",
    "TrackerNote",
    "TrackerRelationship",
    "TrackerRelationshipItem",
    "TrackerTrackedEntity",
]
