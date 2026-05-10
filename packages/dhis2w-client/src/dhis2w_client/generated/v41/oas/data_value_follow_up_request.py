"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .data_value_category_dto import DataValueCategoryDto


class DataValueFollowUpRequest(_BaseModel):
    """OpenAPI schema `DataValueFollowUpRequest`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: DataValueCategoryDto | None = None
    attributeOptionCombo: str | None = _Field(default=None, description="A UID for an CategoryOptionCombo object  ")
    categoryOptionCombo: str | None = _Field(default=None, description="A UID for an CategoryOptionCombo object  ")
    dataElement: str | None = _Field(default=None, description="A UID for an DataSet object  ")
    followup: bool | None = None
    orgUnit: str | None = _Field(default=None, description="A UID for an OrganisationUnit object  ")
    period: str | None = None
