"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .data_value_category_params import DataValueCategoryParams


class DataValuePostParamsPeriod(_BaseModel):
    """OpenAPI schema `DataValuePostParamsPeriod`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataValuePostParams(_BaseModel):
    """OpenAPI schema `DataValuePostParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: DataValueCategoryParams | None = None
    categoryOptionCombo: str | None = None
    comment: str | None = None
    created: datetime | None = None
    dataElement: str | None = None
    dataSet: str | None = None
    followUp: bool | None = None
    force: bool | None = None
    lastUpdated: datetime | None = None
    orgUnit: str | None = None
    period: DataValuePostParamsPeriod | None = None
    storedBy: str | None = None
    value: str | None = None
