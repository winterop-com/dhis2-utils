"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class UserRoleParamsCreatedBy(_BaseModel):
    """OpenAPI schema `UserRoleParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserRoleParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `UserRoleParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserRoleParams(_BaseModel):
    """OpenAPI schema `UserRoleParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    authorities: list[str] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserRoleParamsCreatedBy | None = None
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserRoleParamsLastUpdatedBy | None = None
    name: str | None = None
    restrictions: list[str] | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    users: list[UserDto] | None = None
