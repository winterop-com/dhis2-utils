"""Typed DHIS2 Route `auth` schemes (derived from `/api/openapi.json`).

DHIS2 Routes (integration-proxy metadata objects at `/api/routes`) carry an
`auth` block describing how DHIS2 talks to the upstream target. The OpenAPI
spec models this as a `AuthScheme` polymorphic union discriminated by `type`.

Subtypes (every one DHIS2 v42 accepts):

- `http-basic` -> `HttpBasicAuthScheme` - RFC 7617 Basic auth (user + password).
- `api-token` -> `ApiTokenAuthScheme` - DHIS2-flavour static token.
- `api-headers` -> `ApiHeadersAuthScheme` - arbitrary custom headers.
- `api-query-params` -> `ApiQueryParamsAuthScheme` - auth via query-string params.
- `oauth2-client-credentials` -> `OAuth2ClientCredentialsAuthScheme` - upstream OAuth2 client-credentials flow.

`AuthScheme` is the tagged union — Pydantic picks the right subclass by the
`type` discriminator when you `AuthScheme.model_validate(...)`.

Example:
    >>> scheme = AuthScheme.model_validate({"type": "http-basic", "username": "u", "password": "p"})
    >>> isinstance(scheme, HttpBasicAuthScheme)
    True
    >>> scheme.username
    'u'

Route.auth stays typed as `Any` in the generated `Route` model (DHIS2 schema
limitation). Use `auth_scheme_from_route(route)` to parse it safely.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class HttpBasicAuthScheme(BaseModel):
    """HTTP Basic — `Authorization: Basic base64(username:password)` on upstream calls."""

    model_config = ConfigDict(extra="allow")

    type: Literal["http-basic"] = "http-basic"
    username: str
    password: str


class ApiTokenAuthScheme(BaseModel):
    """Static token — DHIS2 sends `Authorization: ApiToken <token>` (NOT the standard Bearer scheme).

    See BUGS.md #4e for why this is not interchangeable with OAuth2 Bearer tokens.
    """

    model_config = ConfigDict(extra="allow")

    type: Literal["api-token"] = "api-token"
    token: str


class ApiHeadersAuthScheme(BaseModel):
    """Custom header auth — map of header-name to value, e.g. `{"X-Api-Key": "abc"}`."""

    model_config = ConfigDict(extra="allow")

    type: Literal["api-headers"] = "api-headers"
    headers: dict[str, str] = Field(default_factory=dict)


class ApiQueryParamsAuthScheme(BaseModel):
    """Query-string auth — map of param-name to value, e.g. `{"api_key": "abc"}`."""

    model_config = ConfigDict(extra="allow")

    type: Literal["api-query-params"] = "api-query-params"
    queryParams: dict[str, str] = Field(default_factory=dict)


class OAuth2ClientCredentialsAuthScheme(BaseModel):
    """OAuth2 client-credentials — DHIS2 POSTs to `tokenUri` for an access token, caches, then uses it."""

    model_config = ConfigDict(extra="allow")

    type: Literal["oauth2-client-credentials"] = "oauth2-client-credentials"
    clientId: str
    clientSecret: str
    tokenUri: str
    scopes: str | None = None


AuthScheme = Annotated[
    HttpBasicAuthScheme
    | ApiTokenAuthScheme
    | ApiHeadersAuthScheme
    | ApiQueryParamsAuthScheme
    | OAuth2ClientCredentialsAuthScheme,
    Field(discriminator="type"),
]
"""Discriminated union for the 5 DHIS2 Route auth variants. Validate via `AuthSchemeAdapter`."""


AuthSchemeAdapter: TypeAdapter[AuthScheme] = TypeAdapter(AuthScheme)
"""Helper: `AuthSchemeAdapter.validate_python(dict)` picks the right subclass by `type`."""


def auth_scheme_from_route(route: Any) -> AuthScheme | None:
    """Parse a `Route`'s `auth` field into the typed discriminated union.

    The generated `Route.auth` is `Any | None` because DHIS2's `/api/schemas`
    can't express polymorphic unions. This helper reaches into the dict form
    and validates it against the discriminated union — returns `None` when the
    route has no auth block.

    Example:
        >>> route = await client.resources.routes.get("abc123")
        >>> scheme = auth_scheme_from_route(route)
        >>> match scheme:
        ...     case HttpBasicAuthScheme(username=u):
        ...         print(f"basic auth as {u}")
        ...     case OAuth2ClientCredentialsAuthScheme(tokenUri=uri):
        ...         print(f"oauth2 against {uri}")
    """
    raw = getattr(route, "auth", None)
    if raw is None:
        return None
    if isinstance(raw, BaseModel):
        raw = raw.model_dump()
    if not isinstance(raw, dict) or "type" not in raw:
        return None
    return AuthSchemeAdapter.validate_python(raw)


__all__ = [
    "ApiHeadersAuthScheme",
    "ApiQueryParamsAuthScheme",
    "ApiTokenAuthScheme",
    "AuthScheme",
    "AuthSchemeAdapter",
    "HttpBasicAuthScheme",
    "OAuth2ClientCredentialsAuthScheme",
    "auth_scheme_from_route",
]
