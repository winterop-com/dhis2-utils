"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class TrackedEntityDataElementDimensionDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityDataElementDimensionLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityDataElementDimensionProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityDataElementDimension(_BaseModel):
    """OpenAPI schema `TrackedEntityDataElementDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataElement: TrackedEntityDataElementDimensionDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    filter: str | None = None
    legendSet: TrackedEntityDataElementDimensionLegendSet | None = _Field(
        default=None, description="A UID reference to a LegendSet  "
    )
    programStage: TrackedEntityDataElementDimensionProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
