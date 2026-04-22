"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._aliases import Instant
from ._enums import EnrollmentStatus

if TYPE_CHECKING:
    from .event import Event
    from .tracker_attribute import TrackerAttribute
    from .tracker_note import TrackerNote
    from .tracker_relationship import TrackerRelationship
    from .tracker_user import TrackerUser


class TrackerEnrollment(_BaseModel):
    """OpenAPI schema `TrackerEnrollment`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: str | None = None
    attributes: list[TrackerAttribute] | None = None
    completedAt: Instant | None = None
    completedBy: str | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrolledAt: Instant | None = None
    enrollment: str | None = None
    events: list[Event] | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: Instant | None = None
    orgUnit: str | None = None
    program: str | None = None
    relationships: list[TrackerRelationship] | None = None
    status: EnrollmentStatus | None = None
    storedBy: str | None = None
    trackedEntity: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None
