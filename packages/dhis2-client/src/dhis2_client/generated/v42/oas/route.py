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
    from .api_headers_auth_scheme import ApiHeadersAuthScheme
    from .api_query_params_auth_scheme import ApiQueryParamsAuthScheme
    from .api_token_auth_scheme import ApiTokenAuthScheme
    from .attribute_value import AttributeValue
    from .http_basic_auth_scheme import HttpBasicAuthScheme
    from .o_auth2_client_credentials_auth_scheme import OAuth2ClientCredentialsAuthScheme
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class Route(_BaseModel):
    """OpenAPI schema `Route`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    auth: (
        HttpBasicAuthScheme
        | ApiTokenAuthScheme
        | ApiHeadersAuthScheme
        | ApiQueryParamsAuthScheme
        | OAuth2ClientCredentialsAuthScheme
        | None
    ) = None
    authorities: list[str] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    description: str | None = None
    disabled: bool | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    headers: dict[str, str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    name: str | None = None
    responseTimeoutSeconds: int | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    url: str | None = None
