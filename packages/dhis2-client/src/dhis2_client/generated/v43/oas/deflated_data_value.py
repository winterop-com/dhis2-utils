"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class DeflatedDataValuePeriod(_BaseModel):
    """OpenAPI schema `DeflatedDataValuePeriod`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DeflatedDataValue(_BaseModel):
    """OpenAPI schema `DeflatedDataValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionComboId: int | None = None
    categoryOptionComboId: int | None = None
    categoryOptionComboName: str | None = None
    comment: str | None = None
    dataElementId: int | None = None
    dataElementName: str | None = None
    deleted: bool | None = None
    followup: bool | None = None
    max: int | None = None
    min: int | None = None
    period: DeflatedDataValuePeriod | None = None
    periodId: int | None = None
    sourceId: int | None = None
    sourceName: str | None = None
    sourcePath: str | None = None
    value: str | None = None
