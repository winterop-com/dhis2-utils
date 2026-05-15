"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .deprecated__tracker_attribute import DeprecatedTrackerAttribute
    from .deprecated__tracker_event import DeprecatedTrackerEvent
    from .deprecated__tracker_note import DeprecatedTrackerNote
    from .deprecated__tracker_relationship import DeprecatedTrackerRelationship
    from .user_info_snapshot import UserInfoSnapshot


class DeprecatedTrackerEnrollment(_BaseModel):
    """OpenAPI schema `Deprecated_TrackerEnrollment`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[DeprecatedTrackerAttribute] | None = None
    completedBy: str | None = None
    completedDate: datetime | None = None
    created: str | None = None
    createdAtClient: str | None = None
    createdByUserInfo: UserInfoSnapshot | None = None
    deleted: bool | None = None
    enrollment: str | None = None
    enrollmentDate: datetime | None = None
    events: list[DeprecatedTrackerEvent] | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    incidentDate: datetime | None = None
    lastUpdated: str | None = None
    lastUpdatedAtClient: str | None = None
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    notes: list[DeprecatedTrackerNote] | None = None
    orgUnit: str | None = None
    orgUnitName: str | None = None
    program: str | None = None
    relationships: list[DeprecatedTrackerRelationship] | None = None
    status: Literal["ACTIVE", "COMPLETED", "CANCELLED"] | None = None
    storedBy: str | None = None
    trackedEntityInstance: str | None = None
    trackedEntityType: str | None = None
