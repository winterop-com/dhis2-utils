"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import LegendDisplayStrategy, LegendDisplayStyle


class LegendDefinitionsParamsSet(_BaseModel):
    """OpenAPI schema `LegendDefinitionsParamsSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class LegendDefinitionsParams(_BaseModel):
    """OpenAPI schema `LegendDefinitionsParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    set: LegendDefinitionsParamsSet | None = None
    showKey: bool | None = None
    strategy: LegendDisplayStrategy
    style: LegendDisplayStyle
