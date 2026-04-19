"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import LegendDisplayStrategy, LegendDisplayStyle

if TYPE_CHECKING:
    from .legend_set import LegendSet


class LegendDefinitions(_BaseModel):
    """OpenAPI schema `LegendDefinitions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    set: LegendSet | None = None
    showKey: bool | None = None
    strategy: LegendDisplayStrategy
    style: LegendDisplayStyle
