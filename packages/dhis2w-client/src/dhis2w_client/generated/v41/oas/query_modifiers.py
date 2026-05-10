"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class QueryModifiers(_BaseModel):
    """OpenAPI schema `QueryModifiers`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: str | None = None
    maxDate: datetime | None = None
    minDate: datetime | None = None
    periodOffset: int | None = None
    valueType: str | None = None
    yearToDate: bool | None = None
