"""Generated Dhis2OAuth2Client model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Dhis2OAuth2Client(BaseModel):
    """DHIS2 Dhis2OAuth2Client resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    authorizationGrantTypes: str | None = None

    clientAuthenticationMethods: str | None = None

    clientId: str | None = None

    clientIdIssuedAt: datetime | None = None

    clientSecret: str | None = None

    clientSecretExpiresAt: datetime | None = None

    clientSettings: str | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    postLogoutRedirectUris: str | None = None

    redirectUris: str | None = None

    scopes: str | None = None

    sharing: Any | None = None

    tokenSettings: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
