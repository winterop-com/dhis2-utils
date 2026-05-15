"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .tracker_attribute import TrackerAttribute
    from .tracker_data_value import TrackerDataValue
    from .tracker_note import TrackerNote
    from .tracker_program_owner import TrackerProgramOwner
    from .tracker_user import TrackerUser


class TrackerRelationshipItemEnrollment(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemEnrollment`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[TrackerAttribute] | None = None
    completedAt: datetime | int | None = None
    completedBy: str | None = None
    createdAt: datetime | int | None = None
    createdAtClient: datetime | int | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrolledAt: datetime | int | None = None
    enrollment: str | None = _Field(default=None, description="A UID for an Enrollment object  ")
    events: list[TrackerRelationshipItemEnrollmentEvents] | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: datetime | int | None = None
    orgUnit: str | None = None
    program: str | None = None
    status: Literal["ACTIVE", "COMPLETED", "CANCELLED"] | None = None
    storedBy: str | None = None
    trackedEntity: str | None = None
    updatedAt: datetime | int | None = None
    updatedAtClient: datetime | int | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemEnrollmentEvents(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemEnrollmentEvents`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUser: TrackerUser | None = None
    attributeCategoryOptions: str | None = None
    attributeOptionCombo: str | None = None
    completedAt: datetime | int | None = None
    completedBy: str | None = None
    createdAt: datetime | int | None = None
    createdAtClient: datetime | int | None = None
    createdBy: TrackerUser | None = None
    dataValues: list[TrackerDataValue] | None = None
    deleted: bool | None = None
    enrollment: str | None = None
    event: str | None = _Field(default=None, description="A UID for an Event object  ")
    followUp: bool | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: datetime | int | None = None
    orgUnit: str | None = None
    program: str | None = None
    programStage: str | None = None
    scheduledAt: datetime | int | None = None
    status: Literal["ACTIVE", "COMPLETED", "VISITED", "SCHEDULE", "OVERDUE", "SKIPPED"] | None = None
    storedBy: str | None = None
    updatedAt: datetime | int | None = None
    updatedAtClient: datetime | int | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemEvent(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemEvent`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUser: TrackerUser | None = None
    attributeCategoryOptions: str | None = None
    attributeOptionCombo: str | None = None
    completedAt: datetime | int | None = None
    completedBy: str | None = None
    createdAt: datetime | int | None = None
    createdAtClient: datetime | int | None = None
    createdBy: TrackerUser | None = None
    dataValues: list[TrackerDataValue] | None = None
    deleted: bool | None = None
    enrollment: str | None = None
    event: str | None = _Field(default=None, description="A UID for an Event object  ")
    followUp: bool | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: datetime | int | None = None
    orgUnit: str | None = None
    program: str | None = None
    programStage: str | None = None
    scheduledAt: datetime | int | None = None
    status: Literal["ACTIVE", "COMPLETED", "VISITED", "SCHEDULE", "OVERDUE", "SKIPPED"] | None = None
    storedBy: str | None = None
    updatedAt: datetime | int | None = None
    updatedAtClient: datetime | int | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemTrackedEntity(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemTrackedEntity`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[TrackerAttribute] | None = None
    createdAt: datetime | int | None = None
    createdAtClient: datetime | int | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrollments: list[TrackerRelationshipItemTrackedEntityEnrollments] | None = None
    geometry: dict[str, Any] | None = None
    inactive: bool | None = None
    orgUnit: str | None = None
    potentialDuplicate: bool | None = None
    programOwners: list[TrackerProgramOwner] | None = None
    storedBy: str | None = None
    trackedEntity: str | None = _Field(default=None, description="A UID for an TrackedEntity object  ")
    trackedEntityType: str | None = None
    updatedAt: datetime | int | None = None
    updatedAtClient: datetime | int | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemTrackedEntityEnrollments(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemTrackedEntityEnrollments`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[TrackerAttribute] | None = None
    completedAt: datetime | int | None = None
    completedBy: str | None = None
    createdAt: datetime | int | None = None
    createdAtClient: datetime | int | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrolledAt: datetime | int | None = None
    enrollment: str | None = _Field(default=None, description="A UID for an Enrollment object  ")
    events: list[TrackerRelationshipItemTrackedEntityEnrollmentsEvents] | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: datetime | int | None = None
    orgUnit: str | None = None
    program: str | None = None
    status: Literal["ACTIVE", "COMPLETED", "CANCELLED"] | None = None
    storedBy: str | None = None
    trackedEntity: str | None = None
    updatedAt: datetime | int | None = None
    updatedAtClient: datetime | int | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemTrackedEntityEnrollmentsEvents(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemTrackedEntityEnrollmentsEvents`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUser: TrackerUser | None = None
    attributeCategoryOptions: str | None = None
    attributeOptionCombo: str | None = None
    completedAt: datetime | int | None = None
    completedBy: str | None = None
    createdAt: datetime | int | None = None
    createdAtClient: datetime | int | None = None
    createdBy: TrackerUser | None = None
    dataValues: list[TrackerDataValue] | None = None
    deleted: bool | None = None
    enrollment: str | None = None
    event: str | None = _Field(default=None, description="A UID for an Event object  ")
    followUp: bool | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: datetime | int | None = None
    orgUnit: str | None = None
    program: str | None = None
    programStage: str | None = None
    scheduledAt: datetime | int | None = None
    status: Literal["ACTIVE", "COMPLETED", "VISITED", "SCHEDULE", "OVERDUE", "SKIPPED"] | None = None
    storedBy: str | None = None
    updatedAt: datetime | int | None = None
    updatedAtClient: datetime | int | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItem(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enrollment: TrackerRelationshipItemEnrollment | None = None
    event: TrackerRelationshipItemEvent | None = None
    trackedEntity: TrackerRelationshipItemTrackedEntity | None = None
