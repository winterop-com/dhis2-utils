"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class AnalyticsJobParameters(_BaseModel):
    """OpenAPI schema `AnalyticsJobParameters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    lastYears: int | None = None
    skipOutliers: bool | None = None
    skipPrograms: list[str] | None = None
    skipResourceTables: bool | None = None
    skipTableTypes: list[str] | None = None
