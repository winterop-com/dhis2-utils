"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class MinMaxValue(_BaseModel):
    """OpenAPI schema `MinMaxValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryOptionCombo: str | None = _Field(default=None, description="A UID for an CategoryOptionCombo object  ")
    dataElement: str | None = _Field(default=None, description="A UID for an DataElement object  ")
    generated: bool | None = None
    maxValue: int | None = None
    minValue: int | None = None
    orgUnit: str | None = _Field(default=None, description="A UID for an OrganisationUnit object  ")
