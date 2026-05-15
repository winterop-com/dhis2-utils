"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Series(_BaseModel):
    """OpenAPI schema `Series`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    axis: int | None = None
    dimensionItem: str | None = None
    type: (
        Literal[
            "COLUMN",
            "STACKED_COLUMN",
            "BAR",
            "STACKED_BAR",
            "LINE",
            "AREA",
            "STACKED_AREA",
            "PIE",
            "RADAR",
            "GAUGE",
            "YEAR_OVER_YEAR_LINE",
            "YEAR_OVER_YEAR_COLUMN",
            "SCATTER",
            "BUBBLE",
            "SINGLE_VALUE",
            "PIVOT_TABLE",
            "OUTLIER_TABLE",
        ]
        | None
    ) = None
