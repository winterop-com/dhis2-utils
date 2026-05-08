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
    from .option_set_params import OptionSetParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class OptionGroupParamsCreatedBy(_BaseModel):
    """OpenAPI schema `OptionGroupParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `OptionGroupParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupParamsLegendSet(_BaseModel):
    """OpenAPI schema `OptionGroupParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupParamsLegendSets(_BaseModel):
    """OpenAPI schema `OptionGroupParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupParamsOptions(_BaseModel):
    """OpenAPI schema `OptionGroupParamsOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionGroupParams(_BaseModel):
    """OpenAPI schema `OptionGroupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: OptionGroupParamsCreatedBy | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OptionGroupParamsLastUpdatedBy | None = None
    legendSet: OptionGroupParamsLegendSet | None = None
    legendSets: list[OptionGroupParamsLegendSets] | None = None
    name: str | None = None
    optionSet: OptionSetParams | None = None
    options: list[OptionGroupParamsOptions] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
