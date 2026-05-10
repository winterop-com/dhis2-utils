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
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ProgramTrackedEntityAttributeDimensionItemAttribute(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItemCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItemLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItemLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItemProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItemUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItem(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeDimensionItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attribute: ProgramTrackedEntityAttributeDimensionItemAttribute | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramTrackedEntityAttributeDimensionItemCreatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramTrackedEntityAttributeDimensionItemLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    legendSet: ProgramTrackedEntityAttributeDimensionItemLegendSet | None = _Field(
        default=None, description="A UID reference to a LegendSet  "
    )
    program: ProgramTrackedEntityAttributeDimensionItemProgram | None = _Field(
        default=None, description="A UID reference to a Program  "
    )
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    user: ProgramTrackedEntityAttributeDimensionItemUser | None = _Field(
        default=None, description="A UID reference to a User  "
    )
