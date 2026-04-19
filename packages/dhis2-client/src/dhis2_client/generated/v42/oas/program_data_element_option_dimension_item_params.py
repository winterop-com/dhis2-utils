"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .data_element_params import DataElementParams
    from .option_params import OptionParams
    from .program_params import ProgramParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ProgramDataElementOptionDimensionItemParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramDataElementOptionDimensionItemParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementOptionDimensionItemParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramDataElementOptionDimensionItemParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementOptionDimensionItemParamsLegendSet(_BaseModel):
    """OpenAPI schema `ProgramDataElementOptionDimensionItemParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementOptionDimensionItemParams(_BaseModel):
    """OpenAPI schema `ProgramDataElementOptionDimensionItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramDataElementOptionDimensionItemParamsCreatedBy | None = None
    dataElement: DataElementParams | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramDataElementOptionDimensionItemParamsLastUpdatedBy | None = None
    legendSet: ProgramDataElementOptionDimensionItemParamsLegendSet | None = None
    option: OptionParams | None = None
    program: ProgramParams | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    valueType: ValueType | None = None
