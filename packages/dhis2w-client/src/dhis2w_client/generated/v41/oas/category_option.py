"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class CategoryOptionCategories(_BaseModel):
    """A UID reference to a Category  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionCategoryOptionCombos(_BaseModel):
    """A UID reference to a CategoryOptionCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionCategoryOptionGroups(_BaseModel):
    """A UID reference to a CategoryOptionGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOption(_BaseModel):
    """OpenAPI schema `CategoryOption`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: str | None = None
    attributeValues: list[AttributeValue] | None = None
    categories: list[CategoryOptionCategories] | None = None
    categoryOptionCombos: list[CategoryOptionCategoryOptionCombos] | None = None
    categoryOptionGroups: list[CategoryOptionCategoryOptionGroups] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryOptionCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    endDate: datetime | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    isDefault: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryOptionLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    legendSet: CategoryOptionLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[CategoryOptionLegendSets] | None = None
    name: str | None = None
    organisationUnits: list[CategoryOptionOrganisationUnits] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    startDate: datetime | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    user: CategoryOptionUser | None = _Field(default=None, description="A UID reference to a User  ")
