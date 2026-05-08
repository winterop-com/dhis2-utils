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


class Dhis2OAuth2ClientParamsCreatedBy(_BaseModel):
    """OpenAPI schema `Dhis2OAuth2ClientParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Dhis2OAuth2ClientParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `Dhis2OAuth2ClientParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Dhis2OAuth2ClientParams(_BaseModel):
    """OpenAPI schema `Dhis2OAuth2ClientParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    authorizationGrantTypes: str | None = None
    clientAuthenticationMethods: str | None = None
    clientId: str | None = None
    clientIdIssuedAt: datetime | None = None
    clientSecret: str | None = None
    clientSecretExpiresAt: datetime | None = None
    clientSettings: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: Dhis2OAuth2ClientParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: Dhis2OAuth2ClientParamsLastUpdatedBy | None = None
    postLogoutRedirectUris: str | None = None
    redirectUris: str | None = None
    scopes: str | None = None
    sharing: Sharing | None = None
    tokenSettings: str | None = None
    translations: list[Translation] | None = None
