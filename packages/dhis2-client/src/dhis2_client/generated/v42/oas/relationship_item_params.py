"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .enrollment_params import EnrollmentParams
    from .event_params import EventParams
    from .relationship_params import RelationshipParams
    from .tracked_entity_params import TrackedEntityParams


class RelationshipItemParams(_BaseModel):
    """OpenAPI schema `RelationshipItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    enrollment: EnrollmentParams | None = None
    event: EventParams | None = None
    relationship: RelationshipParams | None = None
    trackedEntity: TrackedEntityParams | None = None
