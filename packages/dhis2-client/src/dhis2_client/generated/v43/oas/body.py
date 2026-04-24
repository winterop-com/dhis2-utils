"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .event import Event
    from .tracker_enrollment import TrackerEnrollment
    from .tracker_relationship import TrackerRelationship
    from .tracker_tracked_entity import TrackerTrackedEntity


class Body(_BaseModel):
    """OpenAPI schema `Body`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enrollments: list[TrackerEnrollment] | None = None
    events: list[Event] | None = None
    relationships: list[TrackerRelationship] | None = None
    trackedEntities: list[TrackerTrackedEntity] | None = None
