"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DataDimensionType, ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .dimension_item_keywords_params import DimensionItemKeywordsParams
    from .event_repetition import EventRepetition
    from .legend_set_params import LegendSetParams
    from .program_params import ProgramParams
    from .program_stage_params import ProgramStageParams
    from .sharing import Sharing
    from .translation import Translation


class CategoryParamsCategoryCombos(_BaseModel):
    """OpenAPI schema `CategoryParamsCategoryCombos`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryParamsCategoryOptions(_BaseModel):
    """OpenAPI schema `CategoryParamsCategoryOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryParamsCreatedBy(_BaseModel):
    """OpenAPI schema `CategoryParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryParamsItems(_BaseModel):
    """OpenAPI schema `CategoryParamsItems`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `CategoryParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryParamsOptionSet(_BaseModel):
    """OpenAPI schema `CategoryParamsOptionSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryParams(_BaseModel):
    """OpenAPI schema `CategoryParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType
    allItems: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    categoryCombos: list[CategoryParamsCategoryCombos] | None = None
    categoryOptions: list[CategoryParamsCategoryOptions] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryParamsCreatedBy | None = None
    dataDimension: bool | None = None
    dataDimensionType: DataDimensionType
    description: str | None = None
    dimension: str | None = None
    dimensionItemKeywords: DimensionItemKeywordsParams | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filter: str | None = None
    formName: str | None = None
    id: str | None = None
    items: list[CategoryParamsItems] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryParamsLastUpdatedBy | None = None
    legendSet: LegendSetParams | None = None
    name: str | None = None
    optionSet: CategoryParamsOptionSet | None = None
    program: ProgramParams | None = None
    programStage: ProgramStageParams | None = None
    repetition: EventRepetition | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    valueType: ValueType
