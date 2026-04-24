"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DataAnalysisParams(_BaseModel):
    """OpenAPI schema `DataAnalysisParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    ds: list[str] | None = None
    endDate: str | None = None
    ou: str | None = None
    standardDeviation: float | None = None
    startDate: str | None = None
