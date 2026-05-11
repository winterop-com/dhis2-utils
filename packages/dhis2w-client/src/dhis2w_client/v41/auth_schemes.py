"""Typed DHIS2 Route `auth` schemes — v41 leaves from generated v41 OAS models.

DHIS2's `/api/routes` and `/api/webhooks` objects carry an `auth` block
describing how DHIS2 talks to upstream targets. OpenAPI defines the leaf
schemas — `HttpBasicAuthScheme`, `ApiTokenAuthScheme`, ... — but
historically dropped the Jackson `type` discriminator (BUGS.md #14).

The codegen emitter patches the spec at build time (see
`dhis2w_codegen.spec_patches`) to synthesise the discriminator block +
add a `type: Literal["<tag>"]` field to each variant. This module then
re-exports the generated leaves + the discriminated Union + a TypeAdapter
helper so callers have one import path.

v41 accepts four variants (v42 + v43 added a fifth,
`oauth2-client-credentials`, which v41's runtime + OAS schema don't
carry):

- `http-basic` -> `HttpBasicAuthScheme` - RFC 7617 Basic auth (user + password).
- `api-token` -> `ApiTokenAuthScheme` - DHIS2-flavour static token.
- `api-headers` -> `ApiHeadersAuthScheme` - arbitrary custom headers.
- `api-query-params` -> `ApiQueryParamsAuthScheme` - auth via query-string params.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, TypeAdapter

from dhis2w_client.generated.v41.oas import (
    ApiHeadersAuthScheme as _GeneratedApiHeadersAuthScheme,
)
from dhis2w_client.generated.v41.oas import (
    ApiQueryParamsAuthScheme as _GeneratedApiQueryParamsAuthScheme,
)
from dhis2w_client.generated.v41.oas import (
    ApiTokenAuthScheme as _GeneratedApiTokenAuthScheme,
)
from dhis2w_client.generated.v41.oas import (
    HttpBasicAuthScheme as _GeneratedHttpBasicAuthScheme,
)

# v41's codegen didn't pick up the discriminator spec-patch the v42 + v43
# OAS trees got (see `dhis2w_codegen.spec_patches`), so every leaf carries
# `type: str | None` rather than `type: Literal["<tag>"]`. We rebuild the
# discriminator surface locally — subclass each generated leaf and pin
# `type` to its Literal tag. The wire shape is identical; this just lets
# pydantic's discriminated-union machinery pick the right subclass.


class HttpBasicAuthScheme(_GeneratedHttpBasicAuthScheme):
    """v41 `HttpBasicAuthScheme` with the `type: Literal["http-basic"]` discriminator pinned."""

    type: Literal["http-basic"] = "http-basic"  # pyright: ignore[reportIncompatibleVariableOverride]


class ApiTokenAuthScheme(_GeneratedApiTokenAuthScheme):
    """v41 `ApiTokenAuthScheme` with the `type: Literal["api-token"]` discriminator pinned."""

    type: Literal["api-token"] = "api-token"  # pyright: ignore[reportIncompatibleVariableOverride]


class ApiHeadersAuthScheme(_GeneratedApiHeadersAuthScheme):
    """v41 `ApiHeadersAuthScheme` with the `type: Literal["api-headers"]` discriminator pinned."""

    type: Literal["api-headers"] = "api-headers"  # pyright: ignore[reportIncompatibleVariableOverride]


class ApiQueryParamsAuthScheme(_GeneratedApiQueryParamsAuthScheme):
    """v41 `ApiQueryParamsAuthScheme` with the `type: Literal["api-query-params"]` discriminator pinned."""

    type: Literal["api-query-params"] = "api-query-params"  # pyright: ignore[reportIncompatibleVariableOverride]


AuthScheme = Annotated[
    HttpBasicAuthScheme | ApiTokenAuthScheme | ApiHeadersAuthScheme | ApiQueryParamsAuthScheme,
    Field(discriminator="type"),
]
"""Discriminated union for the 4 DHIS2 v41 Route auth variants. Validate via `AuthSchemeAdapter`."""


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
        ...     case ApiTokenAuthScheme(token=t):
        ...         print(f"api token (length={len(t)})")
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
    "auth_scheme_from_route",
]
