"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, ValueType


class QueryModifiers(_BaseModel):
    """OpenAPI schema `QueryModifiers`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    maxDate: datetime | None = None
    minDate: datetime | None = None
    periodOffset: int | None = None
    valueType: ValueType | None = None
    yearToDate: bool | None = None
