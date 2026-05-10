"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .group import Group


class FormCategoryCombo(_BaseModel):
    """OpenAPI schema `FormCategoryCombo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categories: list[FormCategoryComboCategories] | None = None
    id: str | None = None


class FormCategoryComboCategories(_BaseModel):
    """OpenAPI schema `FormCategoryComboCategories`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryOptions: list[FormCategoryComboCategoriesCategoryOptions] | None = None
    id: str | None = None
    label: str | None = None


class FormCategoryComboCategoriesCategoryOptions(_BaseModel):
    """OpenAPI schema `FormCategoryComboCategoriesCategoryOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    endDate: datetime | None = None
    id: str | None = None
    label: str | None = None
    organisationUnits: list[FormCategoryComboCategoriesCategoryOptionsOrganisationUnits] | None = None
    startDate: datetime | None = None


class FormCategoryComboCategoriesCategoryOptionsOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Form(_BaseModel):
    """OpenAPI schema `Form`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryCombo: FormCategoryCombo | None = None
    groups: list[Group] | None = None
    label: str | None = None
    options: dict[str, dict[str, Any]] | None = None
    subtitle: str | None = None
