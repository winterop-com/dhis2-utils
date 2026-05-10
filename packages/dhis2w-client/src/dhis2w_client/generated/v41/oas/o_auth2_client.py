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
    from .sharing import Sharing
    from .translation import Translation


class OAuth2ClientCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OAuth2ClientLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OAuth2ClientUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OAuth2Client(_BaseModel):
    """OpenAPI schema `OAuth2Client`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    cid: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: OAuth2ClientCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    grantTypes: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OAuth2ClientLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    redirectUris: list[str] | None = None
    secret: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: OAuth2ClientUser | None = _Field(default=None, description="A UID reference to a User  ")
