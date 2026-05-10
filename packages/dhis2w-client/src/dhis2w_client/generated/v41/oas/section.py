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
    from .data_element_operand import DataElementOperand
    from .sharing import Sharing
    from .translation import Translation


class SectionCategoryCombos(_BaseModel):
    """A UID reference to a CategoryCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SectionCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SectionDataElements(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SectionDataSet(_BaseModel):
    """A UID reference to a DataSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SectionIndicators(_BaseModel):
    """A UID reference to a Indicator  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SectionLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SectionUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Section(_BaseModel):
    """OpenAPI schema `Section`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryCombos: list[SectionCategoryCombos] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: SectionCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataElements: list[SectionDataElements] | None = None
    dataSet: SectionDataSet | None = _Field(default=None, description="A UID reference to a DataSet  ")
    description: str | None = None
    disableDataElementAutoGroup: bool | None = None
    displayName: str | None = None
    displayOptions: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    greyedFields: list[DataElementOperand] | None = None
    href: str | None = None
    id: str | None = None
    indicators: list[SectionIndicators] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: SectionLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    sharing: Sharing | None = None
    showColumnTotals: bool | None = None
    showRowTotals: bool | None = None
    sortOrder: int | None = None
    translations: list[Translation] | None = None
    user: SectionUser | None = _Field(default=None, description="A UID reference to a User  ")
