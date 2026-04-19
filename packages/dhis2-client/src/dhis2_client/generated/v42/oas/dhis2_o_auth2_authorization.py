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
    from .user_dto import UserDto


class Dhis2OAuth2Authorization(_BaseModel):
    """OpenAPI schema `Dhis2OAuth2Authorization`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    accessTokenExpiresAt: datetime | None = None
    accessTokenIssuedAt: datetime | None = None
    accessTokenMetadata: str | None = None
    accessTokenScopes: str | None = None
    accessTokenType: str | None = None
    accessTokenValue: str | None = None
    attributeValues: list[AttributeValue] | None = None
    attributes: str | None = None
    authorizationCodeExpiresAt: datetime | None = None
    authorizationCodeIssuedAt: datetime | None = None
    authorizationCodeMetadata: str | None = None
    authorizationCodeValue: str | None = None
    authorizationGrantType: str | None = None
    authorizedScopes: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    deviceCodeExpiresAt: datetime | None = None
    deviceCodeIssuedAt: datetime | None = None
    deviceCodeMetadata: str | None = None
    deviceCodeValue: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    name: str | None = None
    oidcIdTokenClaims: str | None = None
    oidcIdTokenExpiresAt: datetime | None = None
    oidcIdTokenIssuedAt: datetime | None = None
    oidcIdTokenMetadata: str | None = None
    oidcIdTokenValue: str | None = None
    principalName: str | None = None
    refreshTokenExpiresAt: datetime | None = None
    refreshTokenIssuedAt: datetime | None = None
    refreshTokenMetadata: str | None = None
    refreshTokenValue: str | None = None
    registeredClientId: str | None = None
    sharing: Sharing | None = None
    state: str | None = None
    translations: list[Translation] | None = None
    userCodeExpiresAt: datetime | None = None
    userCodeIssuedAt: datetime | None = None
    userCodeMetadata: str | None = None
    userCodeValue: str | None = None
