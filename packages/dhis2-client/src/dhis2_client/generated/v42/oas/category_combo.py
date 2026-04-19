"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DataDimensionType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class CategoryCombo(_BaseModel):
    """OpenAPI schema `CategoryCombo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    categories: list[BaseIdentifiableObject] | None = None
    categoryOptionCombos: list[BaseIdentifiableObject] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataDimensionType: DataDimensionType
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    isDefault: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    name: str | None = None
    sharing: Sharing | None = None
    skipTotal: bool | None = None
    translations: list[Translation] | None = None
