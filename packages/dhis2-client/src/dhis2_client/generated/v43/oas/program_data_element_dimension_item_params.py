"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .data_element_params import DataElementParams
    from .program_params import ProgramParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ProgramDataElementDimensionItemParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramDataElementDimensionItemParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItemParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramDataElementDimensionItemParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItemParamsLegendSet(_BaseModel):
    """OpenAPI schema `ProgramDataElementDimensionItemParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItemParams(_BaseModel):
    """OpenAPI schema `ProgramDataElementDimensionItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramDataElementDimensionItemParamsCreatedBy | None = None
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
    lastUpdatedBy: ProgramDataElementDimensionItemParamsLastUpdatedBy | None = None
    legendSet: ProgramDataElementDimensionItemParamsLegendSet | None = None
    program: ProgramParams | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    valueType: ValueType | None = None
