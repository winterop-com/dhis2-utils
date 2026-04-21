"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import AggregationType, DataDimensionType, ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .dimension_item_keywords_params import DimensionItemKeywordsParams
    from .event_repetition import EventRepetition
    from .legend_set_params import LegendSetParams
    from .option_set_params import OptionSetParams
    from .program_params import ProgramParams
    from .program_stage_params import ProgramStageParams
    from .sharing import Sharing
    from .translation import Translation


class OptionGroupSetParamsCreatedBy(_BaseModel):
    """OpenAPI schema `OptionGroupSetParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetParamsItems(_BaseModel):
    """OpenAPI schema `OptionGroupSetParamsItems`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `OptionGroupSetParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetParamsOptionGroups(_BaseModel):
    """OpenAPI schema `OptionGroupSetParamsOptionGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupSetParams(_BaseModel):
    """OpenAPI schema `OptionGroupSetParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    allItems: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: OptionGroupSetParamsCreatedBy | None = None
    dataDimension: bool | None = None
    dataDimensionType: DataDimensionType | None = None
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
    items: list[OptionGroupSetParamsItems] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OptionGroupSetParamsLastUpdatedBy | None = None
    legendSet: LegendSetParams | None = None
    name: str | None = None
    optionGroups: list[OptionGroupSetParamsOptionGroups] | None = None
    optionSet: OptionSetParams | None = None
    program: ProgramParams | None = None
    programStage: ProgramStageParams | None = None
    repetition: EventRepetition | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    valueType: ValueType | None = None
