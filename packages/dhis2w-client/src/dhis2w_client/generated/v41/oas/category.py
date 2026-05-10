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
    from .dimension_item_keywords import DimensionItemKeywords
    from .event_repetition import EventRepetition
    from .sharing import Sharing
    from .translation import Translation


class CategoryCategoryCombos(_BaseModel):
    """A UID reference to a CategoryCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryCategoryOptions(_BaseModel):
    """A UID reference to a CategoryOption  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryItems(_BaseModel):
    """A UID reference to a DimensionalItemObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionSet(_BaseModel):
    """A UID reference to a OptionSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Category(_BaseModel):
    """OpenAPI schema `Category`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: str | None = None
    allItems: bool | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryCombos: list[CategoryCategoryCombos] | None = None
    categoryOptions: list[CategoryCategoryOptions] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: CategoryCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataDimension: bool | None = None
    dataDimensionType: str | None = None
    description: str | None = None
    dimension: str | None = None
    dimensionItemKeywords: DimensionItemKeywords | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filter: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    items: list[CategoryItems] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: CategoryLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    legendSet: CategoryLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    name: str | None = None
    optionSet: CategoryOptionSet | None = _Field(default=None, description="A UID reference to a OptionSet  ")
    program: CategoryProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programStage: CategoryProgramStage | None = _Field(default=None, description="A UID reference to a ProgramStage  ")
    repetition: EventRepetition | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    user: CategoryUser | None = _Field(default=None, description="A UID reference to a User  ")
    valueType: str | None = None
