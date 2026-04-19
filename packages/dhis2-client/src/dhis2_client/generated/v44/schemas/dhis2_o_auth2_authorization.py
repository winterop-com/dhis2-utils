"""Generated Dhis2OAuth2Authorization model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class Dhis2OAuth2Authorization(BaseModel):
    """Generated model for DHIS2 `Dhis2OAuth2Authorization`.

    DHIS2 Dhis2 O Auth2 Authorization - persisted metadata (generated from /api/schemas at DHIS2 v44).


    API endpoint: /dev/api/oAuth2Authorizations.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    accessTokenExpiresAt: datetime | None = None

    accessTokenIssuedAt: datetime | None = None

    accessTokenMetadata: str | None = None

    accessTokenScopes: str | None = None

    accessTokenType: str | None = None

    accessTokenValue: str | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    attributes: str | None = None

    authorizationCodeExpiresAt: datetime | None = None

    authorizationCodeIssuedAt: datetime | None = None

    authorizationCodeMetadata: str | None = None

    authorizationCodeValue: str | None = None

    authorizationGrantType: str | None = None

    authorizedScopes: str | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    deviceCodeExpiresAt: datetime | None = None

    deviceCodeIssuedAt: datetime | None = None

    deviceCodeMetadata: str | None = None

    deviceCodeValue: str | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

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

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    state: str | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userCodeExpiresAt: datetime | None = None

    userCodeIssuedAt: datetime | None = None

    userCodeMetadata: str | None = None

    userCodeValue: str | None = None
