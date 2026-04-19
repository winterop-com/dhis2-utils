"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._aliases import Instant

if TYPE_CHECKING:
    from .tracker_attribute import TrackerAttribute
    from .tracker_enrollment import TrackerEnrollment
    from .tracker_program_owner import TrackerProgramOwner
    from .tracker_relationship import TrackerRelationship
    from .tracker_user import TrackerUser


class TrackerTrackedEntity(_BaseModel):
    """OpenAPI schema `TrackerTrackedEntity`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributes: list[TrackerAttribute] | None = None
    createdAt: Instant | None = None
    createdAtClient: Instant | None = None
    createdBy: TrackerUser | None = None
    deleted: bool | None = None
    enrollments: list[TrackerEnrollment] | None = None
    geometry: dict[str, Any] | None = None
    inactive: bool | None = None
    orgUnit: str | None = None
    potentialDuplicate: bool | None = None
    programOwners: list[TrackerProgramOwner] | None = None
    relationships: list[TrackerRelationship] | None = None
    storedBy: str | None = None
    trackedEntity: str | None = None
    trackedEntityType: str | None = None
    updatedAt: Instant | None = None
    updatedAtClient: Instant | None = None
    updatedBy: TrackerUser | None = None
