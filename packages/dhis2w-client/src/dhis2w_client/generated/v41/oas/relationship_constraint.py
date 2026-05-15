"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .tracker_data_view import TrackerDataView


class RelationshipConstraintProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipConstraintProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipConstraintTrackedEntityType(_BaseModel):
    """A UID reference to a TrackedEntityType  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipConstraint(_BaseModel):
    """OpenAPI schema `RelationshipConstraint`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    program: RelationshipConstraintProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programStage: RelationshipConstraintProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    relationshipEntity: Literal["TRACKED_ENTITY_INSTANCE", "PROGRAM_INSTANCE", "PROGRAM_STAGE_INSTANCE"] | None = None
    trackedEntityType: RelationshipConstraintTrackedEntityType | None = _Field(
        default=None, description="A UID reference to a TrackedEntityType  "
    )
    trackerDataView: TrackerDataView | None = None
