"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DataDimensionType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class CategoryComboParamsCategories(_BaseModel):
    """OpenAPI schema `CategoryComboParamsCategories`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryComboParamsCategoryOptionCombos(_BaseModel):
    """OpenAPI schema `CategoryComboParamsCategoryOptionCombos`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryComboParamsCreatedBy(_BaseModel):
    """OpenAPI schema `CategoryComboParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryComboParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `CategoryComboParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryComboParams(_BaseModel):
    """OpenAPI schema `CategoryComboParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    categories: list[CategoryComboParamsCategories] | None = None
    categoryOptionCombos: list[CategoryComboParamsCategoryOptionCombos] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryComboParamsCreatedBy | None = None
    dataDimensionType: DataDimensionType | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    isDefault: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryComboParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    skipTotal: bool | None = None
    translations: list[Translation] | None = None
