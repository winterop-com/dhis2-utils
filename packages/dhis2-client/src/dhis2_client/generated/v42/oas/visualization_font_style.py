"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .font_style import FontStyle


class VisualizationFontStyle(_BaseModel):
    """OpenAPI schema `VisualizationFontStyle`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    baseLineLabel: FontStyle | None = None
    categoryAxisLabel: FontStyle | None = None
    horizontalAxisTitle: FontStyle | None = None
    legend: FontStyle | None = None
    seriesAxisLabel: FontStyle | None = None
    targetLineLabel: FontStyle | None = None
    verticalAxisTitle: FontStyle | None = None
    visualizationSubtitle: FontStyle | None = None
    visualizationTitle: FontStyle | None = None
