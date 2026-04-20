"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class CategoryOptionParamsCategories(_BaseModel):
    """OpenAPI schema `CategoryOptionParamsCategories`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionParamsCategoryOptionCombos(_BaseModel):
    """OpenAPI schema `CategoryOptionParamsCategoryOptionCombos`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionParamsCategoryOptionGroups(_BaseModel):
    """OpenAPI schema `CategoryOptionParamsCategoryOptionGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionParamsCreatedBy(_BaseModel):
    """OpenAPI schema `CategoryOptionParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `CategoryOptionParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `CategoryOptionParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionParams(_BaseModel):
    """OpenAPI schema `CategoryOptionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    categories: list[CategoryOptionParamsCategories] | None = None
    categoryOptionCombos: list[CategoryOptionParamsCategoryOptionCombos] | None = None
    categoryOptionGroups: list[CategoryOptionParamsCategoryOptionGroups] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryOptionParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    endDate: datetime | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    isDefault: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryOptionParamsLastUpdatedBy | None = None
    name: str | None = None
    organisationUnits: list[CategoryOptionParamsOrganisationUnits] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    startDate: datetime | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
