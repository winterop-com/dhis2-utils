"""Typed DHIS2 Route `auth` schemes (shim over generated/v42/oas).

DHIS2 Routes (integration-proxy metadata objects at `/api/routes`) carry an
`auth` block describing how DHIS2 talks to the upstream target. OpenAPI ships
the 5 leaf types as standalone schemas under `components/schemas/*AuthScheme`
but doesn't encode the discriminator — `type` is absent from the OAS output.

This module subclasses each OAS leaf, adds the `type: Literal[...]`
discriminator with the right wire tag, and composes the tagged union plus
`AuthSchemeAdapter` on top. DHIS2 picks the right variant by the `type`
value on both reads and writes.

Subtypes (every one DHIS2 v42 accepts):

- `http-basic` -> `HttpBasicAuthScheme` - RFC 7617 Basic auth (user + password).
- `api-token` -> `ApiTokenAuthScheme` - DHIS2-flavour static token.
- `api-headers` -> `ApiHeadersAuthScheme` - arbitrary custom headers.
- `api-query-params` -> `ApiQueryParamsAuthScheme` - auth via query-string params.
- `oauth2-client-credentials` -> `OAuth2ClientCredentialsAuthScheme` - upstream OAuth2 client-credentials flow.

`Route.auth` stays typed as `Any` in the generated `Route` model (DHIS2
`/api/schemas` can't express polymorphic unions). Use
`auth_scheme_from_route(route)` to parse it safely.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, TypeAdapter

from dhis2_client.generated.v42.oas import (
    ApiHeadersAuthScheme as _ApiHeadersAuthScheme,
)
from dhis2_client.generated.v42.oas import (
    ApiQueryParamsAuthScheme as _ApiQueryParamsAuthScheme,
)
from dhis2_client.generated.v42.oas import (
    ApiTokenAuthScheme as _ApiTokenAuthScheme,
)
from dhis2_client.generated.v42.oas import (
    HttpBasicAuthScheme as _HttpBasicAuthScheme,
)
from dhis2_client.generated.v42.oas import (
    OAuth2ClientCredentialsAuthScheme as _OAuth2ClientCredentialsAuthScheme,
)


class HttpBasicAuthScheme(_HttpBasicAuthScheme):
    """HTTP Basic — `Authorization: Basic base64(username:password)` on upstream calls."""

    type: Literal["http-basic"] = "http-basic"


class ApiTokenAuthScheme(_ApiTokenAuthScheme):
    """Static token — DHIS2 sends `Authorization: ApiToken <token>` (NOT the standard Bearer scheme).

    See BUGS.md #4e for why this is not interchangeable with OAuth2 Bearer tokens.
    """

    type: Literal["api-token"] = "api-token"


class ApiHeadersAuthScheme(_ApiHeadersAuthScheme):
    """Custom header auth — map of header-name to value, e.g. `{"X-Api-Key": "abc"}`."""

    type: Literal["api-headers"] = "api-headers"


class ApiQueryParamsAuthScheme(_ApiQueryParamsAuthScheme):
    """Query-string auth — map of param-name to value, e.g. `{"api_key": "abc"}`."""

    type: Literal["api-query-params"] = "api-query-params"


class OAuth2ClientCredentialsAuthScheme(_OAuth2ClientCredentialsAuthScheme):
    """OAuth2 client-credentials — DHIS2 POSTs to `tokenUri` for an access token, caches, then uses it.

    OpenAPI omits `scopes` from the schema but DHIS2 accepts it on writes
    and returns it on reads. Adding it back here so callers get the typed
    field without relying on `extra="allow"`.
    """

    type: Literal["oauth2-client-credentials"] = "oauth2-client-credentials"
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
