"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, MissingValueStrategy

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ExpressionDimensionItemParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ExpressionDimensionItemParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExpressionDimensionItemParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ExpressionDimensionItemParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExpressionDimensionItemParamsLegendSet(_BaseModel):
    """OpenAPI schema `ExpressionDimensionItemParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExpressionDimensionItemParamsLegendSets(_BaseModel):
    """OpenAPI schema `ExpressionDimensionItemParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ExpressionDimensionItemParams(_BaseModel):
    """OpenAPI schema `ExpressionDimensionItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ExpressionDimensionItemParamsCreatedBy | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    expression: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ExpressionDimensionItemParamsLastUpdatedBy | None = None
    legendSet: ExpressionDimensionItemParamsLegendSet | None = None
    legendSets: list[ExpressionDimensionItemParamsLegendSets] | None = None
    missingValueStrategy: MissingValueStrategy | None = None
    name: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    slidingWindow: bool | None = None
    translations: list[Translation] | None = None
