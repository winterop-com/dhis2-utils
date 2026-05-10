"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class TrackedEntityAttributeDimensionAttribute(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeDimensionLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeDimension(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: TrackedEntityAttributeDimensionAttribute | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
    filter: str | None = None
    legendSet: TrackedEntityAttributeDimensionLegendSet | None = _Field(
        default=None, description="A UID reference to a LegendSet  "
    )
