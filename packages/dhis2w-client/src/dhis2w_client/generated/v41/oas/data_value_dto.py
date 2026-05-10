"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .data_value_category_dto import DataValueCategoryDto


class DataValueDto(_BaseModel):
    """OpenAPI schema `DataValueDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: DataValueCategoryDto | None = None
    categoryOptionCombo: str | None = _Field(default=None, description="A UID for an CategoryOptionCombo object  ")
    comment: str | None = None
    created: datetime | None = None
    dataElement: str | None = _Field(default=None, description="A UID for an DataElement object  ")
    dataSet: str | None = _Field(default=None, description="A UID for an DataSet object  ")
    followUp: bool | None = None
    force: bool | None = None
    lastUpdated: datetime | None = None
    orgUnit: str | None = _Field(default=None, description="A UID for an OrganisationUnit object  ")
    period: str | None = None
    storedBy: str | None = None
    value: str | None = None
