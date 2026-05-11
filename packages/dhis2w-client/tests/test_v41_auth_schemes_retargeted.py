"""v41 Route auth schemes target `generated.v41.oas` (4 variants, no oauth2-client-credentials)."""

from __future__ import annotations


def test_v41_auth_scheme_classes_subclass_v41_generated_tree() -> None:
    """The 4 v41 auth-scheme classes are local subclasses pinning the discriminator on top of v41 generated bases."""
    import dhis2w_client.v41.auth_schemes as v41_auth_schemes
    from dhis2w_client.generated.v41.oas import (
        ApiHeadersAuthScheme as GenApiHeadersAuthScheme,
    )
    from dhis2w_client.generated.v41.oas import (
        ApiQueryParamsAuthScheme as GenApiQueryParamsAuthScheme,
    )
    from dhis2w_client.generated.v41.oas import (
        ApiTokenAuthScheme as GenApiTokenAuthScheme,
    )
    from dhis2w_client.generated.v41.oas import (
        HttpBasicAuthScheme as GenHttpBasicAuthScheme,
    )

    assert issubclass(v41_auth_schemes.HttpBasicAuthScheme, GenHttpBasicAuthScheme)
    assert issubclass(v41_auth_schemes.ApiTokenAuthScheme, GenApiTokenAuthScheme)
    assert issubclass(v41_auth_schemes.ApiHeadersAuthScheme, GenApiHeadersAuthScheme)
    assert issubclass(v41_auth_schemes.ApiQueryParamsAuthScheme, GenApiQueryParamsAuthScheme)
    # The local subclasses live in the v41 module (not the generated tree).
    assert v41_auth_schemes.HttpBasicAuthScheme.__module__ == "dhis2w_client.v41.auth_schemes"


def test_v41_auth_scheme_discriminator_picks_subclass_from_wire_type() -> None:
    """The discriminated union picks the right subclass from `type` on the v41 local subclasses."""
    from dhis2w_client.v41.auth_schemes import (
        ApiTokenAuthScheme,
        AuthSchemeAdapter,
        HttpBasicAuthScheme,
    )

    parsed_basic = AuthSchemeAdapter.validate_python({"type": "http-basic", "username": "u", "password": "p"})
    assert isinstance(parsed_basic, HttpBasicAuthScheme)
    parsed_token = AuthSchemeAdapter.validate_python({"type": "api-token", "token": "tok"})
    assert isinstance(parsed_token, ApiTokenAuthScheme)


def test_v41_does_not_expose_oauth2_client_credentials_scheme() -> None:
    """v41 doesn't accept `oauth2-client-credentials` auth on Routes."""
    import dhis2w_client.v41.auth_schemes as auth_schemes_module

    assert not hasattr(auth_schemes_module, "OAuth2ClientCredentialsAuthScheme")
    assert "OAuth2ClientCredentialsAuthScheme" not in auth_schemes_module.__all__


def test_v42_keeps_oauth2_client_credentials_scheme() -> None:
    """v42's sibling still exposes the 5th variant (sanity check)."""
    import dhis2w_client.v42.auth_schemes as auth_schemes_module

    assert hasattr(auth_schemes_module, "OAuth2ClientCredentialsAuthScheme")
    assert "OAuth2ClientCredentialsAuthScheme" in auth_schemes_module.__all__
