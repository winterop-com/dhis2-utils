"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .filter_options import FilterOptions


class EmbeddedOptions(_BaseModel):
    """OpenAPI schema `EmbeddedOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    filters: FilterOptions | None = None
    hideChartControls: bool | None = None
    hideTab: bool | None = None
