"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .indicator_type_params import IndicatorTypeParams
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class IndicatorParamsCreatedBy(_BaseModel):
    """OpenAPI schema `IndicatorParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorParamsDataSets(_BaseModel):
    """OpenAPI schema `IndicatorParamsDataSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorParamsIndicatorGroups(_BaseModel):
    """OpenAPI schema `IndicatorParamsIndicatorGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `IndicatorParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorParamsLegendSet(_BaseModel):
    """OpenAPI schema `IndicatorParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorParamsLegendSets(_BaseModel):
    """OpenAPI schema `IndicatorParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IndicatorParams(_BaseModel):
    """OpenAPI schema `IndicatorParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: AggregationType | None = None
    annualized: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: IndicatorParamsCreatedBy | None = None
    dataSets: list[IndicatorParamsDataSets] | None = None
    decimals: int | None = None
    denominator: str | None = None
    denominatorDescription: str | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDenominatorDescription: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayNumeratorDescription: str | None = None
    displayShortName: str | None = None
    explodedDenominator: str | None = None
    explodedNumerator: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    indicatorGroups: list[IndicatorParamsIndicatorGroups] | None = None
    indicatorType: IndicatorTypeParams | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: IndicatorParamsLastUpdatedBy | None = None
    legendSet: IndicatorParamsLegendSet | None = None
    legendSets: list[IndicatorParamsLegendSets] | None = None
    name: str | None = None
    numerator: str | None = None
    numeratorDescription: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    url: str | None = None
