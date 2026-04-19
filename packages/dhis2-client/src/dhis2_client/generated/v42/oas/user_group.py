"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class UserGroup(_BaseModel):
    """OpenAPI schema `UserGroup`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    managedByGroups: list[BaseIdentifiableObject] | None = None
    managedGroups: list[BaseIdentifiableObject] | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    users: list[UserDto] | None = None
