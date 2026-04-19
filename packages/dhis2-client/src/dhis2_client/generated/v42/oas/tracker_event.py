"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._aliases import Instant
from ._enums import EventStatus

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
    relationships: list[TrackerRelationship] | None = None
    scheduledAt: Instant | None = None
    status: EventStatus | None = None
    storedBy: str | None = None
    trackedEntity: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None
