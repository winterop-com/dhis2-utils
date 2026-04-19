"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DataDimensionType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class CategoryOptionGroupParamsCategoryOptions(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupParamsCategoryOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupParamsCreatedBy(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupParamsGroupSets(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupParamsGroupSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupParamsLegendSet(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupParamsLegendSets(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupParams(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValueParams] | None = None
    categoryOptions: list[CategoryOptionGroupParamsCategoryOptions] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryOptionGroupParamsCreatedBy | None = None
    dataDimensionType: DataDimensionType | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    groupSets: list[CategoryOptionGroupParamsGroupSets] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryOptionGroupParamsLastUpdatedBy | None = None
    legendSet: CategoryOptionGroupParamsLegendSet | None = None
    legendSets: list[CategoryOptionGroupParamsLegendSets] | None = None
    name: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
