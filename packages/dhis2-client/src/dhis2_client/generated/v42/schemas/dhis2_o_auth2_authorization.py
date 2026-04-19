"""Generated Dhis2OAuth2Authorization model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class Dhis2OAuth2Authorization(BaseModel):
    """Generated model for DHIS2 `Dhis2OAuth2Authorization`.

    DHIS2 Dhis2 O Auth2 Authorization - persisted metadata (generated from /api/schemas at DHIS2 v42).


    API endpoint: /api/oAuth2Authorizations.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    accessTokenExpiresAt: datetime | None = None

    accessTokenIssuedAt: datetime | None = None

    accessTokenMetadata: str | None = Field(default=None, description="Length/value max=2147483647.")

    accessTokenScopes: str | None = Field(default=None, description="Length/value max=1000.")

    accessTokenType: str | None = Field(default=None, description="Length/value max=255.")

    accessTokenValue: str | None = Field(default=None, description="Length/value max=4000.")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    attributes: str | None = Field(default=None, description="Length/value max=2147483647.")

    authorizationCodeExpiresAt: datetime | None = None

    authorizationCodeIssuedAt: datetime | None = None

    authorizationCodeMetadata: str | None = Field(default=None, description="Length/value max=2147483647.")

    authorizationCodeValue: str | None = Field(default=None, description="Length/value max=4000.")

    authorizationGrantType: str | None = Field(default=None, description="Length/value max=255.")

    authorizedScopes: str | None = Field(default=None, description="Length/value max=1000.")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    deviceCodeExpiresAt: datetime | None = None

    deviceCodeIssuedAt: datetime | None = None

    deviceCodeMetadata: str | None = Field(default=None, description="Length/value max=2147483647.")

    deviceCodeValue: str | None = Field(default=None, description="Length/value max=4000.")

    displayName: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    oidcIdTokenClaims: str | None = Field(default=None, description="Length/value max=2147483647.")

    oidcIdTokenExpiresAt: datetime | None = None

    oidcIdTokenIssuedAt: datetime | None = None

    oidcIdTokenMetadata: str | None = Field(default=None, description="Length/value max=2147483647.")

    oidcIdTokenValue: str | None = Field(default=None, description="Length/value max=4000.")

    principalName: str | None = Field(default=None, description="Length/value max=255.")

    refreshTokenExpiresAt: datetime | None = None

    refreshTokenIssuedAt: datetime | None = None

    refreshTokenMetadata: str | None = Field(default=None, description="Length/value max=2147483647.")

    refreshTokenValue: str | None = Field(default=None, description="Length/value max=4000.")

    registeredClientId: str | None = Field(default=None, description="Length/value max=255.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    state: str | None = Field(default=None, description="Length/value max=500.")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userCodeExpiresAt: datetime | None = None

    userCodeIssuedAt: datetime | None = None

    userCodeMetadata: str | None = Field(default=None, description="Length/value max=2147483647.")

    userCodeValue: str | None = Field(default=None, description="Length/value max=4000.")
