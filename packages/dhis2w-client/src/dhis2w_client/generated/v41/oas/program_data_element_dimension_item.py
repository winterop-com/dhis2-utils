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


class ProgramDataElementDimensionItemCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItemDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItemLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItemLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItemProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItemUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramDataElementDimensionItem(_BaseModel):
    """OpenAPI schema `ProgramDataElementDimensionItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramDataElementDimensionItemCreatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    dataElement: ProgramDataElementDimensionItemDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramDataElementDimensionItemLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    legendSet: ProgramDataElementDimensionItemLegendSet | None = _Field(
        default=None, description="A UID reference to a LegendSet  "
    )
    program: ProgramDataElementDimensionItemProgram | None = _Field(
        default=None, description="A UID reference to a Program  "
    )
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: ProgramDataElementDimensionItemUser | None = _Field(default=None, description="A UID reference to a User  ")
    valueType: str | None = None
