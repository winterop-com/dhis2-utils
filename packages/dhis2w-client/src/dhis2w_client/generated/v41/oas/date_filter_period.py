"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DateFilterPeriod(_BaseModel):
    """OpenAPI schema `DateFilterPeriod`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    endBuffer: int | None = None
    endDate: datetime | None = None
    period: str | None = None
    startBuffer: int | None = None
    startDate: datetime | None = None
    type: str | None = None
