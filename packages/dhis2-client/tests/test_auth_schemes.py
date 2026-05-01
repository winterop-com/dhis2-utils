"""Unit tests for the AuthScheme discriminated union + Route helper."""

from __future__ import annotations

from dhis2_client.auth_schemes import (
    ApiHeadersAuthScheme,
    ApiQueryParamsAuthScheme,
    ApiTokenAuthScheme,
    AuthSchemeAdapter,
    HttpBasicAuthScheme,
    OAuth2ClientCredentialsAuthScheme,
    auth_scheme_from_route,
)
from pydantic import BaseModel


def test_validate_picks_http_basic() -> None:
    scheme = AuthSchemeAdapter.validate_python({"type": "http-basic", "username": "alice", "password": "secret"})
    assert isinstance(scheme, HttpBasicAuthScheme)
    assert scheme.username == "alice"


def test_validate_picks_api_token() -> None:
    scheme = AuthSchemeAdapter.validate_python({"type": "api-token", "token": "tkn"})
    assert isinstance(scheme, ApiTokenAuthScheme)
    assert scheme.token == "tkn"


def test_validate_picks_api_headers() -> None:
    scheme = AuthSchemeAdapter.validate_python({"type": "api-headers", "headers": {"X-Api-Key": "abc"}})
    assert isinstance(scheme, ApiHeadersAuthScheme)
    assert scheme.headers is not None
    assert scheme.headers["X-Api-Key"] == "abc"


def test_validate_picks_api_query_params() -> None:
    scheme = AuthSchemeAdapter.validate_python({"type": "api-query-params", "queryParams": {"api_key": "abc"}})
    assert isinstance(scheme, ApiQueryParamsAuthScheme)
    assert scheme.queryParams is not None
    assert scheme.queryParams["api_key"] == "abc"


def test_validate_picks_oauth2_client_credentials() -> None:
    scheme = AuthSchemeAdapter.validate_python(
        {
            "type": "oauth2-client-credentials",
            "clientId": "cid",
            "clientSecret": "cs",
            "tokenUri": "https://auth.example/oauth2/token",
            "scopes": "read write",
        }
    )
    assert isinstance(scheme, OAuth2ClientCredentialsAuthScheme)
    assert scheme.clientId == "cid"
    assert scheme.scopes == "read write"


def test_round_trip_preserves_discriminator() -> None:
    """A scheme dumps with its `type` field so the same dict can be re-validated."""
    original = HttpBasicAuthScheme(username="u", password="p")
    dumped = original.model_dump()
    assert dumped["type"] == "http-basic"
    reparsed = AuthSchemeAdapter.validate_python(dumped)
    assert isinstance(reparsed, HttpBasicAuthScheme)
    assert reparsed.username == "u"


class _MockRoute(BaseModel):
    """Stand-in for the generated `Route` model — only the `auth` field matters for the helper."""

    auth: object = None


def test_auth_scheme_from_route_handles_dict_auth() -> None:
    route = _MockRoute(auth={"type": "http-basic", "username": "u", "password": "p"})
    scheme = auth_scheme_from_route(route)
    assert isinstance(scheme, HttpBasicAuthScheme)


def test_auth_scheme_from_route_handles_missing_auth() -> None:
    route = _MockRoute(auth=None)
    assert auth_scheme_from_route(route) is None


def test_auth_scheme_from_route_handles_missing_type() -> None:
    route = _MockRoute(auth={"username": "u"})
    assert auth_scheme_from_route(route) is None
