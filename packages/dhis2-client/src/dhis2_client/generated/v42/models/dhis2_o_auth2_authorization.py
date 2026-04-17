"""Generated Dhis2OAuth2Authorization model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Dhis2OAuth2Authorization(BaseModel):
    """DHIS2 Dhis2OAuth2Authorization resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    accessTokenExpiresAt: datetime | None = None

    accessTokenIssuedAt: datetime | None = None

    accessTokenMetadata: str | None = None

    accessTokenScopes: str | None = None

    accessTokenType: str | None = None

    accessTokenValue: str | None = None

    attributeValues: Any | None = None

    attributes: str | None = None

    authorizationCodeExpiresAt: datetime | None = None

    authorizationCodeIssuedAt: datetime | None = None

    authorizationCodeMetadata: str | None = None

    authorizationCodeValue: str | None = None

    authorizationGrantType: str | None = None

    authorizedScopes: str | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    deviceCodeExpiresAt: datetime | None = None

    deviceCodeIssuedAt: datetime | None = None

    deviceCodeMetadata: str | None = None

    deviceCodeValue: str | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

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

    sharing: Any | None = None

    state: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    userCodeExpiresAt: datetime | None = None

    userCodeIssuedAt: datetime | None = None

    userCodeMetadata: str | None = None

    userCodeValue: str | None = None
