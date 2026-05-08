"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .legend_set_params import LegendSetParams
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams


class TrackedEntityAttributeDimensionParams(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeDimensionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: TrackedEntityAttributeParams | None = None
    filter: str | None = None
    legendSet: LegendSetParams | None = None
