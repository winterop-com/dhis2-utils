"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .deprecated__tracker_attribute import DeprecatedTrackerAttribute
    from .deprecated__tracker_enrollment import DeprecatedTrackerEnrollment
    from .deprecated__tracker_program_owner import DeprecatedTrackerProgramOwner
    from .deprecated__tracker_relationship import DeprecatedTrackerRelationship
    from .user_info_snapshot import UserInfoSnapshot


class DeprecatedTrackerTrackedEntityInstance(_BaseModel):
    """OpenAPI schema `Deprecated_TrackerTrackedEntityInstance`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[DeprecatedTrackerAttribute] | None = None
    coordinates: str | None = None
    created: str | None = None
    createdAtClient: str | None = None
    createdByUserInfo: UserInfoSnapshot | None = None
    deleted: bool | None = None
    enrollments: list[DeprecatedTrackerEnrollment] | None = None
    featureType: Literal["NONE", "MULTI_POLYGON", "POLYGON", "POINT", "SYMBOL"] | None = None
    geometry: dict[str, Any] | None = None
    inactive: bool | None = None
    lastUpdated: str | None = None
    lastUpdatedAtClient: str | None = None
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    orgUnit: str | None = None
    potentialDuplicate: bool | None = None
    programOwners: list[DeprecatedTrackerProgramOwner] | None = None
    relationships: list[DeprecatedTrackerRelationship] | None = None
    storedBy: str | None = None
    trackedEntityInstance: str | None = None
    trackedEntityType: str | None = None
