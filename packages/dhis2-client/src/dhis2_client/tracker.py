"""Typed models for DHIS2 tracker instance data.

Metadata resources (`/api/schemas`) don't cover tracker *instance* shapes —
those live at `/api/tracker/*` and are described only in the OpenAPI spec.
These pydantic models are hand-written from `/api/openapi.json#/components/schemas`
and use `extra="allow"` everywhere so new DHIS2 fields don't break callers.

Models here cover the cases our service layer touches:

| DHIS2 schema         | Class                    | Endpoint                              |
|----------------------|--------------------------|----------------------------------------|
| TrackerTrackedEntity | `TrackerTrackedEntity`   | `/api/tracker/trackedEntities`        |
| TrackerEnrollment    | `TrackerEnrollment`      | `/api/tracker/enrollments`            |
| TrackerEvent         | `TrackerEvent`           | `/api/tracker/events`                 |
| RelationshipItem     | `TrackerRelationship`    | `/api/tracker/relationships`          |

Status enums (`EnrollmentStatus`, `EventStatus`) are the exact values DHIS2
uses on the wire; `StrEnum` keeps them round-trippable through JSON.
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


__all__ = [
    "EnrollmentStatus",
    "EventStatus",
    "TrackerAttributeValue",
    "TrackerDataValue",
    "TrackerEnrollment",
    "TrackerEvent",
    "TrackerNote",
    "TrackerRelationship",
    "TrackerRelationshipItem",
    "TrackerTrackedEntity",
]
