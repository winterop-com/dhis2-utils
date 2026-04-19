"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import AggregationType, DimensionItemType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class SubexpressionDimensionItemParamsCreatedBy(_BaseModel):
    """OpenAPI schema `SubexpressionDimensionItemParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SubexpressionDimensionItemParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `SubexpressionDimensionItemParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SubexpressionDimensionItemParamsLegendSet(_BaseModel):
    """OpenAPI schema `SubexpressionDimensionItemParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SubexpressionDimensionItemParamsLegendSets(_BaseModel):
    """OpenAPI schema `SubexpressionDimensionItemParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SubexpressionDimensionItemParams(_BaseModel):
    """OpenAPI schema `SubexpressionDimensionItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: SubexpressionDimensionItemParamsCreatedBy | None = None
    description: str | None = None
    dimensionItem: str | None = None
    dimensionItemType: DimensionItemType | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: SubexpressionDimensionItemParamsLastUpdatedBy | None = None
    legendSet: SubexpressionDimensionItemParamsLegendSet | None = None
    legendSets: list[SubexpressionDimensionItemParamsLegendSets] | None = None
    name: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
