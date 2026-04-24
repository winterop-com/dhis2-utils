"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import RelationshipEntity

if TYPE_CHECKING:
    from .program import Program
    from .program_stage import ProgramStage
    from .tracked_entity_type import TrackedEntityType
    from .tracker_data_view import TrackerDataView


class RelationshipConstraint(_BaseModel):
    """OpenAPI schema `RelationshipConstraint`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    program: Program | None = None
    programStage: ProgramStage | None = None
    relationshipEntity: RelationshipEntity | None = None
    trackedEntityType: TrackedEntityType | None = None
    trackerDataView: TrackerDataView | None = None
