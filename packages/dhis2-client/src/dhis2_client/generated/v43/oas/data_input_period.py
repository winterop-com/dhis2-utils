"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DataInputPeriodPeriod(_BaseModel):
    """OpenAPI schema `DataInputPeriodPeriod`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataInputPeriod(_BaseModel):
    """OpenAPI schema `DataInputPeriod`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    closingDate: datetime | None = None
    openingDate: datetime | None = None
    period: DataInputPeriodPeriod | None = None
