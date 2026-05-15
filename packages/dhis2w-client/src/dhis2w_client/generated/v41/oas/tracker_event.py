"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .tracker_data_value import TrackerDataValue
    from .tracker_note import TrackerNote
    from .tracker_relationship import TrackerRelationship
    from .tracker_user import TrackerUser


class TrackerEvent(_BaseModel):
    """OpenAPI schema `TrackerEvent`."""

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
    enrollment: str | None = _Field(default=None, description="A UID for an TrackerEnrollment object  ")
    event: str | None = _Field(default=None, description="A UID for an TrackerEvent object  ")
    followUp: bool | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    notes: list[TrackerNote] | None = None
    occurredAt: datetime | int | None = None
    orgUnit: str | None = None
    program: str | None = None
    programStage: str | None = None
    relationships: list[TrackerRelationship] | None = None
    scheduledAt: datetime | int | None = None
    status: Literal["ACTIVE", "COMPLETED", "VISITED", "SCHEDULE", "OVERDUE", "SKIPPED"] | None = None
    storedBy: str | None = None
    trackedEntity: str | None = _Field(default=None, description="A UID for an TrackerTrackedEntity object  ")
    updatedAt: datetime | int | None = None
    updatedAtClient: datetime | int | None = None
    updatedBy: TrackerUser | None = None
