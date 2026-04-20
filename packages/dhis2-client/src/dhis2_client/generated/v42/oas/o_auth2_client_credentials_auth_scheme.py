"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class OAuth2ClientCredentialsAuthScheme(_BaseModel):
    """OpenAPI schema `OAuth2ClientCredentialsAuthScheme`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    clientId: str | None = None
    clientSecret: str | None = None
    scopes: str | None = None
    tokenUri: str | None = None
    type: Literal["oauth2-client-credentials"] = "oauth2-client-credentials"
