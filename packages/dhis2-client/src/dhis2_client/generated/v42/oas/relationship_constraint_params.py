"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import RelationshipEntity

if TYPE_CHECKING:
    from .tracker_data_view import TrackerDataView


class RelationshipConstraintParamsProgram(_BaseModel):
    """OpenAPI schema `RelationshipConstraintParamsProgram`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipConstraintParamsProgramStage(_BaseModel):
    """OpenAPI schema `RelationshipConstraintParamsProgramStage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipConstraintParamsTrackedEntityType(_BaseModel):
    """OpenAPI schema `RelationshipConstraintParamsTrackedEntityType`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipConstraintParams(_BaseModel):
    """OpenAPI schema `RelationshipConstraintParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    program: RelationshipConstraintParamsProgram | None = None
    programStage: RelationshipConstraintParamsProgramStage | None = None
    relationshipEntity: RelationshipEntity | None = None
    trackedEntityType: RelationshipConstraintParamsTrackedEntityType | None = None
    trackerDataView: TrackerDataView | None = None
