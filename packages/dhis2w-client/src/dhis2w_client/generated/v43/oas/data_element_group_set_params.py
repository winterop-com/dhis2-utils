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


class DataElementGroupSetParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataElementGroupSetParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupSetParamsDataElementGroups(_BaseModel):
    """OpenAPI schema `DataElementGroupSetParamsDataElementGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupSetParamsItems(_BaseModel):
    """OpenAPI schema `DataElementGroupSetParamsItems`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupSetParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataElementGroupSetParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupSetParamsOptionSet(_BaseModel):
    """OpenAPI schema `DataElementGroupSetParamsOptionSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupSetParams(_BaseModel):
    """OpenAPI schema `DataElementGroupSetParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    allItems: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    compulsory: bool | None = None
    created: datetime | None = None
    createdBy: DataElementGroupSetParamsCreatedBy | None = None
    dataDimension: bool | None = None
    dataDimensionType: DataDimensionType | None = None
    dataElementGroups: list[DataElementGroupSetParamsDataElementGroups] | None = None
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
    items: list[DataElementGroupSetParamsItems] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataElementGroupSetParamsLastUpdatedBy | None = None
    legendSet: LegendSetParams | None = None
    name: str | None = None
    optionSet: DataElementGroupSetParamsOptionSet | None = None
    program: ProgramParams | None = None
    programStage: ProgramStageParams | None = None
    repetition: EventRepetition | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    valueType: ValueType | None = None
