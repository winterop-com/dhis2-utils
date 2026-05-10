"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .api_headers_auth_scheme import ApiHeadersAuthScheme
    from .api_query_params_auth_scheme import ApiQueryParamsAuthScheme
    from .api_token_auth_scheme import ApiTokenAuthScheme
    from .http_basic_auth_scheme import HttpBasicAuthScheme


class WebhookTarget(_BaseModel):
    """OpenAPI schema `WebhookTarget`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    auth: HttpBasicAuthScheme | ApiTokenAuthScheme | ApiHeadersAuthScheme | ApiQueryParamsAuthScheme | None = None
    clientId: str | None = None
    contentType: str | None = None
    headers: dict[str, str] | None = None
    type: str | None = None
    url: str | None = None
