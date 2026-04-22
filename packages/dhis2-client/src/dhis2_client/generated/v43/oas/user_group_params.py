"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class UserGroupParamsCreatedBy(_BaseModel):
    """OpenAPI schema `UserGroupParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserGroupParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `UserGroupParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserGroupParamsManagedByGroups(_BaseModel):
    """OpenAPI schema `UserGroupParamsManagedByGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserGroupParamsManagedGroups(_BaseModel):
    """OpenAPI schema `UserGroupParamsManagedGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserGroupParams(_BaseModel):
    """OpenAPI schema `UserGroupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserGroupParamsCreatedBy | None = None
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserGroupParamsLastUpdatedBy | None = None
    managedByGroups: list[UserGroupParamsManagedByGroups] | None = None
    managedGroups: list[UserGroupParamsManagedGroups] | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    users: list[UserDto] | None = None
