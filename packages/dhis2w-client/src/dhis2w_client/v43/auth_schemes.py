"""Typed DHIS2 Route `auth` schemes — re-exports from generated v42 OAS models.

DHIS2's `/api/routes` and `/api/webhooks` objects carry an `auth` block
describing how DHIS2 talks to upstream targets. OpenAPI defines the five
leaf schemas — `HttpBasicAuthScheme`, `ApiTokenAuthScheme`, ... — but
historically dropped the Jackson `type` discriminator (BUGS.md #14).

The codegen emitter patches the spec at build time (see
`dhis2w_codegen.spec_patches`) to synthesise the discriminator block +
add a `type: Literal["<tag>"]` field to each variant. This module then
re-exports the generated leaves + the discriminated Union + a TypeAdapter
helper so callers have one import path.

Subtypes (every one DHIS2 v42 accepts):

- `http-basic` -> `HttpBasicAuthScheme` - RFC 7617 Basic auth (user + password).
- `api-token` -> `ApiTokenAuthScheme` - DHIS2-flavour static token.
- `api-headers` -> `ApiHeadersAuthScheme` - arbitrary custom headers.
- `api-query-params` -> `ApiQueryParamsAuthScheme` - auth via query-string params.
- `oauth2-client-credentials` -> `OAuth2ClientCredentialsAuthScheme` - upstream OAuth2 client-credentials flow.
"""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import BaseModel, Field, TypeAdapter

from dhis2w_client.generated.v43.oas import (
    ApiHeadersAuthScheme,
    ApiQueryParamsAuthScheme,
    ApiTokenAuthScheme,
    HttpBasicAuthScheme,
    OAuth2ClientCredentialsAuthScheme,
)

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

    Since the codegen spec-patches sweep `Route.auth` is already the
    discriminated Union; this helper exists for legacy callers that pass
    in a raw dict (e.g. loaded from JSON or from a pre-patched spec).

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
