"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DeflatedDataValue(_BaseModel):
    """OpenAPI schema `DeflatedDataValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionComboId: int
    categoryOptionComboId: int
    categoryOptionComboName: str | None = None
    comment: str | None = None
    dataElementId: int
    dataElementName: str | None = None
    deleted: bool | None = None
    followup: bool | None = None
    max: int
    min: int
    period: str | None = None
    periodId: int
    sourceId: int
    sourceName: str | None = None
    sourcePath: str | None = None
    value: str | None = None
