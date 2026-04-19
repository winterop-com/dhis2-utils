"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class LegendParamsCreatedBy(_BaseModel):
    """OpenAPI schema `LegendParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class LegendParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `LegendParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class LegendParams(_BaseModel):
    """OpenAPI schema `LegendParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    color: str | None = None
    created: datetime | None = None
    createdBy: LegendParamsCreatedBy | None = None
    displayName: str | None = None
    endValue: float | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    image: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: LegendParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    startValue: float | None = None
    translations: list[Translation] | None = None
