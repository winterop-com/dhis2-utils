"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class TrackedEntityProgramIndicatorDimensionLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityProgramIndicatorDimensionProgramIndicator(_BaseModel):
    """A UID reference to a ProgramIndicator  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityProgramIndicatorDimension(_BaseModel):
    """OpenAPI schema `TrackedEntityProgramIndicatorDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    filter: str | None = None
    legendSet: TrackedEntityProgramIndicatorDimensionLegendSet | None = _Field(
        default=None, description="A UID reference to a LegendSet  "
    )
    programIndicator: TrackedEntityProgramIndicatorDimensionProgramIndicator | None = _Field(
        default=None, description="A UID reference to a ProgramIndicator  "
    )
