"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DimensionItemType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .category_combo_params import CategoryComboParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class CategoryOptionComboParamsCategoryOptions(_BaseModel):
    """OpenAPI schema `CategoryOptionComboParamsCategoryOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryOptionComboParamsCreatedBy(_BaseModel):
    """OpenAPI schema `CategoryOptionComboParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryOptionComboParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `CategoryOptionComboParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryOptionComboParamsLegendSet(_BaseModel):
    """OpenAPI schema `CategoryOptionComboParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryOptionComboParamsLegendSets(_BaseModel):
    """OpenAPI schema `CategoryOptionComboParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryOptionComboParams(_BaseModel):
    """OpenAPI schema `CategoryOptionComboParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType
    attributeValues: list[AttributeValueParams] | None = None
    categoryCombo: CategoryComboParams | None = None
    categoryOptions: list[CategoryOptionComboParamsCategoryOptions] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryOptionComboParamsCreatedBy | None = None
    description: str | None = None
    dimensionItem: str | None = None
    dimensionItemType: DimensionItemType
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    ignoreApproval: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryOptionComboParamsLastUpdatedBy | None = None
    legendSet: CategoryOptionComboParamsLegendSet | None = None
    legendSets: list[CategoryOptionComboParamsLegendSets] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
