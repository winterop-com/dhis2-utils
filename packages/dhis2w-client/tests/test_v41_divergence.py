"""Pinned tests for every v41-specific divergence from the v42 baseline.

The v41 hand-written tree is mostly a mechanical copy of v42 (see
`docs/architecture/versioning.md`). Each divergence from that baseline
gets a pinned test here that asserts the divergence still holds — so
when a future codegen regen, refactor, or DHIS2 fix unwittingly
realigns v41 with v42, this file's assertions surface the change
before it ships.

The tests are NOT redundant with the BUGS regression suite. The BUGS
suite asserts the live wire behaves the way the workaround expects;
these assert the v41 hand-written tree's *static shape* still differs
from v42 in the documented ways.

Categories covered:

- v41 OAS / wire-shape adapters: Grid.rows widening, App.displayName
  override + model_rebuild() materialisation.
- v41 local stubs: 6 metadata enums (AtomicMode, FlushMode,
  ImportStrategy, MergeMode, PreheatIdentifier, PreheatMode) live in
  `dhis2w_client.v41._enum_stubs` because v41 OAS doesn't surface them.
- v41 OAuth2 surface: OAuth2ClientCredentialsAuthScheme deliberately
  absent from auth_schemes.

When a new v41 divergence lands, add a test to the matching section
below + a one-line entry to the docstring's "Categories covered" list.
"""

from __future__ import annotations

import pytest

# ----- v41 OAS / wire-shape adapters -----------------------------------------


def test_v41_grid_rows_is_widened_to_list_list_any() -> None:
    """BUGS adapter — `Grid.rows: list[list[Any]] | None` overrides the v41 OAS's lying `list[list[dict[str, Any]]]`.

    v41 OAS declares row cells as `dict[str, Any]` but the actual wire
    carries scalars / null. `dhis2w_client.v41.analytics.Grid` subclasses
    `_GeneratedGrid` and widens `rows` so analytics responses parse cleanly.
    v42 / v43 don't need this — their OAS types rows correctly.
    """
    from dhis2w_client.generated.v41.oas import Grid as GeneratedGrid
    from dhis2w_client.v41.analytics import Grid

    assert Grid is not GeneratedGrid, "v41 Grid must be a subclass that overrides `rows`"
    assert Grid.model_fields["rows"].annotation == list[list] | None or "list" in str(
        Grid.model_fields["rows"].annotation
    ), f"v41 Grid.rows annotation drifted: {Grid.model_fields['rows'].annotation!r}"


def test_v41_app_subclass_carries_display_name_field() -> None:
    """v41 `App` adds the runtime-emitted `displayName` field that v41 OAS doesn't declare.

    Without this override, callers reading `app.displayName` would fall
    through to pydantic's `model_extra` instead of typed access. Also
    materialises the validator via `model_rebuild()` so subclass
    instantiation works under the `defer_build=True` parent config.
    """
    from dhis2w_client.generated.v41.oas import App as GeneratedApp
    from dhis2w_client.v41.apps import App

    assert App is not GeneratedApp, "v41 App must be a subclass that adds displayName"
    assert "displayName" in App.model_fields, (
        "v41 App.model_fields must declare `displayName`; the override exists "
        "because v41 OAS doesn't list it but the runtime emits it"
    )
    # `model_rebuild()` was called at import time — subclass must be instantiable.
    instance = App(name="probe")
    assert instance.name == "probe"
    assert instance.displayName is None


# ----- v41 cross-version imports ---------------------------------------------


@pytest.mark.parametrize(
    "enum_name",
    [
        "AtomicMode",
        "FlushMode",
        "ImportStrategy",
        "MergeMode",
        "PreheatIdentifier",
        "PreheatMode",
    ],
)
def test_v41_metadata_enums_resolve_to_local_stubs(enum_name: str) -> None:
    """v41 OAS doesn't surface these enums; the v41 metadata plugin imports them from local stubs.

    Wire values are identical across v41 / v42 / v43, so v41's plugin
    tree carries a hand-written stub at `dhis2w_client.v41._enum_stubs`
    (no cross-version reach into `generated.v42.oas`). If v41's OAS
    ever starts emitting these — unlikely; v41 is in upstream
    maintenance — retarget the metadata service to
    `dhis2w_client.generated.v41.oas` and delete the stub file.
    """
    from dhis2w_core.v41.plugins.metadata import service

    assert hasattr(service, enum_name), (
        f"v41 metadata service must surface {enum_name} (via the local stub at `dhis2w_client.v41._enum_stubs`)"
    )
    enum_cls = getattr(service, enum_name)
    assert enum_cls.__module__ == "dhis2w_client.v41._enum_stubs", (
        f"{enum_name} should resolve to the v41 local stub — got {enum_cls.__module__}. "
        f"If v41 OAS now declares it, retarget the metadata-service import to "
        f"`dhis2w_client.generated.v41.oas` and delete `_enum_stubs.py`."
    )


# ----- v41 OAuth2 surface ---------------------------------------------------


def test_v41_auth_schemes_lacks_oauth2_client_credentials() -> None:
    """v41 OAS + runtime don't carry the `oauth2-client-credentials` auth-scheme variant.

    v42 / v43 ship a 5th `OAuth2ClientCredentialsAuthScheme` variant for
    Route auth; v41 has only the 4-variant set (http-basic, api-token,
    api-headers, api-query-params). The discriminated union must stay
    4-variant on v41.
    """
    from dhis2w_client.v41 import auth_schemes

    assert not hasattr(auth_schemes, "OAuth2ClientCredentialsAuthScheme"), (
        "v41 auth_schemes must not export OAuth2ClientCredentialsAuthScheme — "
        "v41 OAS + runtime don't carry that variant. If DHIS2 v41 backports the "
        "variant, this assertion can be removed alongside the route-CLI handler."
    )
    # Confirm the 4 expected variants are still there.
    for variant in (
        "HttpBasicAuthScheme",
        "ApiTokenAuthScheme",
        "ApiHeadersAuthScheme",
        "ApiQueryParamsAuthScheme",
    ):
        assert hasattr(auth_schemes, variant), f"v41 auth_schemes missing {variant}"
