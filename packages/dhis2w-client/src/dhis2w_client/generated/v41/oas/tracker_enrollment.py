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
    from .tracker_event import TrackerEvent
    from .tracker_note import TrackerNote
    from .tracker_relationship import TrackerRelationship
    from .tracker_user import TrackerUser


class TrackerEnrollment(_BaseModel):
    """OpenAPI schema `TrackerEnrollment`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[TrackerAttribute] | None = None
    completedAt: datetime | int | None = None
    completedBy: str | None = None
    createdAt: datetime | int | None = None
    createdAtClient: datetime | int | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrolledAt: datetime | int | None = None
    enrollment: str | None = _Field(default=None, description="A UID for an TrackerEnrollment object  ")
    events: list[TrackerEvent] | None = None
    followUp: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: datetime | int | None = None
    orgUnit: str | None = None
    program: str | None = None
    relationships: list[TrackerRelationship] | None = None
    status: Literal["ACTIVE", "COMPLETED", "CANCELLED"] | None = None
    storedBy: str | None = None
    trackedEntity: str | None = _Field(default=None, description="A UID for an TrackerTrackedEntity object  ")
    updatedAt: datetime | int | None = None
    updatedAtClient: datetime | int | None = None
    updatedBy: TrackerUser | None = None
