"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .legend_params import LegendParams
    from .sharing import Sharing
    from .translation import Translation


class LegendSetParamsCreatedBy(_BaseModel):
    """OpenAPI schema `LegendSetParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class LegendSetParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `LegendSetParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class LegendSetParams(_BaseModel):
    """OpenAPI schema `LegendSetParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: LegendSetParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: LegendSetParamsLastUpdatedBy | None = None
    legends: list[LegendParams] | None = None
    name: str | None = None
    sharing: Sharing | None = None
    symbolizer: str | None = None
    translations: list[Translation] | None = None
