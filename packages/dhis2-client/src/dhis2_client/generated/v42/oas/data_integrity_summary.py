"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class DataIntegritySummary(_BaseModel):
    """OpenAPI schema `DataIntegritySummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    count: int | None = None
    error: str | None = None
    finishedTime: datetime | None = None
    percentage: float | None = None
    startTime: datetime | None = None
