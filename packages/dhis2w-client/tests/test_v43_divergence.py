"""Pinned tests for every v43-specific divergence from the v42 baseline.

Mirror of `test_v41_divergence.py` for the v43 hand-written tree. Each
asserts the static shape of a known v43 divergence so future refactors
or codegen regens that accidentally realign with v42 surface here.

Categories covered:

- v43 wire-shape adapters: `SharingObject.externalAccess` dropped,
  `SharingBuilder` no longer accepts `external_access`.
- v43 CategoryCombo: `categorys` legacy alias dropped from the
  write-payload path (`categories` is the sole field name).

Mocked-then-live coverage for these landed earlier as BUGS regression
tests (paired `test_bug_3{4,8}_*` in `test_upstream_bugs.py`); this
file's tests stay structural — they don't hit the wire, they just
assert the v43 source code shape stayed divergent.

When a new v43 divergence lands, add a test below + a one-line entry
to "Categories covered".
"""

from __future__ import annotations

import inspect

# ----- v43 wire-shape adapters ----------------------------------------------


def test_v43_sharing_object_lacks_external_access_field() -> None:
    """v43's `SharingObject` doesn't carry `externalAccess` (the wire schema dropped it)."""
    from dhis2w_client.v43.sharing import SharingObject

    assert "externalAccess" not in SharingObject.model_fields, (
        "v43 SharingObject must not declare `externalAccess` — the wire schema "
        "dropped it. If DHIS2 v43 reintroduces the field, regenerate codegen + "
        "update `dhis2w_client.v43.sharing` + drop this assertion."
    )


def test_v43_sharing_builder_does_not_accept_external_access() -> None:
    """v43's `SharingBuilder.__init__` doesn't take `external_access` (v42 has it; v43 dropped)."""
    from dhis2w_client.v43.sharing import SharingBuilder

    init_params = inspect.signature(SharingBuilder).parameters
    assert "external_access" not in init_params, (
        "v43 SharingBuilder must not accept `external_access` — v43 wire dropped "
        f"the field. Got params: {list(init_params)}"
    )
    # Confirm the v43 builder still has the expected v43 surface.
    assert "public_access" in init_params
    assert "owner_user_id" in init_params


# ----- v43 CategoryCombo ----------------------------------------------------


def test_v43_category_combo_create_payload_uses_categories_key() -> None:
    """v43 `CategoryCombosAccessor.create` POSTs `categories` (wire spelling), not the v42 `categorys` alias.

    v43 dropped the historical `categorys` alias. Inspects the
    `create` method's source body to confirm the payload key is the
    wire-correct `categories`. (The module-level docstring still
    mentions `categorys` to explain the historical alias — that's fine,
    we only care about the actual POST payload.)
    """
    from dhis2w_client.v43.category_combos import CategoryCombosAccessor

    create_source = inspect.getsource(CategoryCombosAccessor.create)
    # The payload dict literal must include the `categories` key and must NOT
    # include the misspelled `categorys` alias.
    assert '"categories":' in create_source, (
        f'v43 CategoryCombosAccessor.create must build a `"categories":` payload key. Source body:\n{create_source}'
    )
    assert '"categorys":' not in create_source, (
        f'v43 CategoryCombosAccessor.create must not use the v42 `"categorys":` alias — '
        f"v43 silently no-ops on it (BUGS.md #34). Source body:\n{create_source}"
    )
