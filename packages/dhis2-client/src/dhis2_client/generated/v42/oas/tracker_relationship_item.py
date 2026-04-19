"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._aliases import Instant
from ._enums import EnrollmentStatus, EventStatus

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
    completedAt: Instant | None = None
    completedBy: str | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrolledAt: Instant | None = None
    enrollment: str | None = None
    events: list[TrackerRelationshipItemEnrollmentEvents] | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: Instant | None = None
    orgUnit: str | None = None
    program: str | None = None
    status: EnrollmentStatus
    storedBy: str | None = None
    trackedEntity: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemEnrollmentEvents(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemEnrollmentEvents`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUser: TrackerUser | None = None
    attributeCategoryOptions: str | None = None
    attributeOptionCombo: str | None = None
    completedAt: Instant | None = None
    completedBy: str | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    createdBy: TrackerUser | None = None
    dataValues: list[TrackerDataValue] | None = None
    deleted: bool | None = None
    enrollment: str | None = None
    event: str | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: Instant | None = None
    orgUnit: str | None = None
    program: str | None = None
    programStage: str | None = None
    scheduledAt: Instant | None = None
    status: EventStatus
    storedBy: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemEvent(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemEvent`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUser: TrackerUser | None = None
    attributeCategoryOptions: str | None = None
    attributeOptionCombo: str | None = None
    completedAt: Instant | None = None
    completedBy: str | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    createdBy: TrackerUser | None = None
    dataValues: list[TrackerDataValue] | None = None
    deleted: bool | None = None
    enrollment: str | None = None
    event: str | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: Instant | None = None
    orgUnit: str | None = None
    program: str | None = None
    programStage: str | None = None
    scheduledAt: Instant | None = None
    status: EventStatus
    storedBy: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemTrackedEntity(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemTrackedEntity`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[TrackerAttribute] | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrollments: list[TrackerRelationshipItemTrackedEntityEnrollments] | None = None
    geometry: dict[str, Any] | None = None
    inactive: bool | None = None
    orgUnit: str | None = None
    potentialDuplicate: bool | None = None
    programOwners: list[TrackerProgramOwner] | None = None
    storedBy: str | None = None
    trackedEntity: str | None = None
    trackedEntityType: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemTrackedEntityEnrollments(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemTrackedEntityEnrollments`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[TrackerAttribute] | None = None
    completedAt: Instant | None = None
    completedBy: str | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrolledAt: Instant | None = None
    enrollment: str | None = None
    events: list[TrackerRelationshipItemTrackedEntityEnrollmentsEvents] | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: Instant | None = None
    orgUnit: str | None = None
    program: str | None = None
    status: EnrollmentStatus
    storedBy: str | None = None
    trackedEntity: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItemTrackedEntityEnrollmentsEvents(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItemTrackedEntityEnrollmentsEvents`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUser: TrackerUser | None = None
    attributeCategoryOptions: str | None = None
    attributeOptionCombo: str | None = None
    completedAt: Instant | None = None
    completedBy: str | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    createdBy: TrackerUser | None = None
    dataValues: list[TrackerDataValue] | None = None
    deleted: bool | None = None
    enrollment: str | None = None
    event: str | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: Instant | None = None
    orgUnit: str | None = None
    program: str | None = None
    programStage: str | None = None
    scheduledAt: Instant | None = None
    status: EventStatus
    storedBy: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None


class TrackerRelationshipItem(_BaseModel):
    """OpenAPI schema `TrackerRelationshipItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enrollment: TrackerRelationshipItemEnrollment | None = None
    event: TrackerRelationshipItemEvent | None = None
    trackedEntity: TrackerRelationshipItemTrackedEntity | None = None
