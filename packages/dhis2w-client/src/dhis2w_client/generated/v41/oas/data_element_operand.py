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


class DataElementOperandAttributeOptionCombo(_BaseModel):
    """A UID reference to a CategoryOptionCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandCategoryOptionCombo(_BaseModel):
    """A UID reference to a CategoryOptionCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperand(_BaseModel):
    """OpenAPI schema `DataElementOperand`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeOptionCombo: DataElementOperandAttributeOptionCombo | None = _Field(
        default=None, description="A UID reference to a CategoryOptionCombo  "
    )
    attributeValues: list[AttributeValue] | None = None
    categoryOptionCombo: DataElementOperandCategoryOptionCombo | None = _Field(
        default=None, description="A UID reference to a CategoryOptionCombo  "
    )
    code: str | None = None
    created: datetime | None = None
    createdBy: DataElementOperandCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataElement: DataElementOperandDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataElementOperandLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    legendSet: DataElementOperandLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[DataElementOperandLegendSets] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: DataElementOperandUser | None = _Field(default=None, description="A UID reference to a User  ")
