"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .deprecated__tracker_enrollment import DeprecatedTrackerEnrollment
    from .deprecated__tracker_event import DeprecatedTrackerEvent
    from .deprecated__tracker_tracked_entity_instance import DeprecatedTrackerTrackedEntityInstance


class DeprecatedTrackerRelationshipItem(_BaseModel):
    """OpenAPI schema `Deprecated_TrackerRelationshipItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enrollment: DeprecatedTrackerEnrollment | None = None
    event: DeprecatedTrackerEvent | None = None
    trackedEntityInstance: DeprecatedTrackerTrackedEntityInstance | None = None
