"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .deprecated__tracker_data_value import DeprecatedTrackerDataValue
    from .deprecated__tracker_note import DeprecatedTrackerNote
    from .deprecated__tracker_relationship import DeprecatedTrackerRelationship
    from .user_info_snapshot import UserInfoSnapshot


class DeprecatedTrackerEvent(_BaseModel):
    """OpenAPI schema `Deprecated_TrackerEvent`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignedUser: str | None = None
    assignedUserDisplayName: str | None = None
    assignedUserFirstName: str | None = None
    assignedUserSurname: str | None = None
    assignedUserUsername: str | None = None
    attributeCategoryOptions: str | None = None
    attributeOptionCombo: str | None = None
    completedBy: str | None = None
    completedDate: str | None = None
    created: str | None = None
    createdAtClient: str | None = None
    createdByUserInfo: UserInfoSnapshot | None = None
    dataValues: list[DeprecatedTrackerDataValue] | None = None
    deleted: bool | None = None
    dueDate: str | None = None
    enrollment: str | None = None
    enrollmentStatus: Literal["ACTIVE", "COMPLETED", "CANCELLED"] | None = None
    event: str | None = None
    eventDate: str | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    href: str | None = None
    lastUpdated: str | None = None
    lastUpdatedAtClient: str | None = None
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    notes: list[DeprecatedTrackerNote] | None = None
    orgUnit: str | None = None
    orgUnitName: str | None = None
    program: str | None = None
    programStage: str | None = None
    programType: Literal["WITH_REGISTRATION", "WITHOUT_REGISTRATION"] | None = None
    relationships: list[DeprecatedTrackerRelationship] | None = None
    status: Literal["ACTIVE", "COMPLETED", "VISITED", "SCHEDULE", "OVERDUE", "SKIPPED"] | None = None
    storedBy: str | None = None
    trackedEntityInstance: str | None = None
