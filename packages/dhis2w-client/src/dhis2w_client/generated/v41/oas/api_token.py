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
    from .ip_allowed_list import IpAllowedList
    from .method_allowed_list import MethodAllowedList
    from .referer_allowed_list import RefererAllowedList
    from .sharing import Sharing
    from .translation import Translation


class ApiTokenCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ApiTokenLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ApiTokenUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ApiToken(_BaseModel):
    """OpenAPI schema `ApiToken`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    attributes: list[IpAllowedList | RefererAllowedList | MethodAllowedList] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ApiTokenCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    expire: int | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ApiTokenLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    type: str | None = None
    user: ApiTokenUser | None = _Field(default=None, description="A UID reference to a User  ")
    version: int | None = None
