"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class MinMaxDataElementParamsDataElement(_BaseModel):
    """OpenAPI schema `MinMaxDataElementParamsDataElement`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MinMaxDataElementParamsOptionCombo(_BaseModel):
    """OpenAPI schema `MinMaxDataElementParamsOptionCombo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MinMaxDataElementParamsSource(_BaseModel):
    """OpenAPI schema `MinMaxDataElementParamsSource`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MinMaxDataElementParams(_BaseModel):
    """OpenAPI schema `MinMaxDataElementParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataElement: MinMaxDataElementParamsDataElement | None = None
    generated: bool | None = None
    max: int
    min: int
    optionCombo: MinMaxDataElementParamsOptionCombo | None = None
    source: MinMaxDataElementParamsSource | None = None
