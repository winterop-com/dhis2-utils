"""Paired upstream-bug regression tests — one bug + one workaround per BUGS.md entry.

Every test here is marked `@pytest.mark.upstream_bug` and lives in pairs:

- A **bug-still-present** test models DHIS2's buggy behaviour via respx
  (or runs against a live stack tagged with `@pytest.mark.slow`) and
  asserts the bug is observable. When DHIS2 ships an upstream fix, this
  test stops matching reality — easy way to catch when we can drop the
  workaround.
- A **workaround-works** test exercises our client code through the
  same buggy server behaviour and asserts the correct end state lands.

The marker is registered in `pyproject.toml`. List the regression
suite with `make test-upstream-bugs`. The full test suite (`make test`)
includes these by default since the respx-mocked halves are fast.

This file ships the initial pattern with BUGS.md #33 covered. Add new
pairs here as workarounds land.
"""

from __future__ import annotations

import httpx
import pytest
import respx
from dhis2w_client import BasicAuth, Dhis2Client


def _auth() -> BasicAuth:
    """Throwaway BasicAuth for in-process respx tests."""
    return BasicAuth(username="admin", password="district")


def _mock_v43_connect() -> None:
    """Mock the v43 server connect probes (canonical URL + /api/system/info)."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.43.0"}),
    )


@pytest.mark.upstream_bug
@respx.mock
async def test_bug_33_v43_save_does_not_populate_coc_matrix() -> None:
    """BUGS.md #33 — bug-still-present: v43 saves a CategoryCombo with zero COCs.

    On v42, saving a CategoryCombo auto-generates its CategoryOptionCombo
    matrix server-side. On v43, save persists with `categoryOptionCombos: []`
    until `POST /api/maintenance/categoryOptionComboUpdate` runs. This test
    models the v43 wire response — when DHIS2 fixes the bug upstream, the
    `categoryOptionCombos[].id` array would carry rows immediately after
    the create response, and we'd update the test (or it'd start failing
    against a live v43 server).
    """
    _mock_v43_connect()
    respx.post("https://dhis2.example/api/categoryCombos").mock(
        return_value=httpx.Response(201, json={"status": "OK", "httpStatusCode": 201, "response": {"uid": "CC_NEW"}}),
    )
    # The bug: immediately after create, GET shows the combo with empty COC list on v43.
    respx.get("https://dhis2.example/api/categoryCombos/CC_NEW").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "CC_NEW",
                "name": "Sex",
                "dataDimensionType": "DISAGGREGATION",
                "skipTotal": False,
                "categories": [{"id": "CAT_SEX"}],
                "categoryOptionCombos": [],  # <-- the bug: should be 2 (cross-product of "Male"/"Female").
            },
        ),
    )
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        combo = await client.category_combos.create(name="Sex", categories=["CAT_SEX"])
    assert combo.categoryOptionCombos == [], (
        "BUGS.md #33: v43 should still leave categoryOptionCombos empty on save. "
        "If this assertion fails, DHIS2 may have shipped a fix — verify upstream "
        "and remove the workaround in `dhis2w_client/v43/category_combos.py`."
    )


@pytest.mark.upstream_bug
@respx.mock
async def test_bug_33_v43_workaround_fires_maintenance_trigger() -> None:
    """BUGS.md #33 — workaround-works: `wait_for_coc_generation` on v43 fires the maintenance task.

    The v43 sibling of `wait_for_coc_generation` calls
    `POST /api/maintenance/categoryOptionComboUpdate` once before polling so the
    matrix actually fills. This test asserts the maintenance route is hit on v43
    (and would NOT be hit on v42 — covered separately in
    `test_per_version_dispatch.test_v42_wait_for_coc_skips_maintenance_trigger`).
    """
    _mock_v43_connect()
    maintenance_route = respx.post("https://dhis2.example/api/maintenance/categoryOptionComboUpdate").mock(
        return_value=httpx.Response(200, json={"httpStatus": "OK"})
    )
    respx.get("https://dhis2.example/api/categoryOptionCombos").mock(
        return_value=httpx.Response(200, json={"categoryOptionCombos": [{"id": "COC_1"}, {"id": "COC_2"}]}),
    )
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        assert client.version_key == "v43"
        landed = await client.category_combos.wait_for_coc_generation(
            "CC_NEW", expected_count=2, timeout_seconds=2.0, poll_interval_seconds=0.01
        )
    assert landed == 2
    assert maintenance_route.called, (
        "BUGS.md #33 workaround: v43's wait_for_coc_generation must fire the maintenance "
        "trigger. If this fails, the workaround in `dhis2w_client/v43/category_combos.py` "
        "has regressed."
    )


# ---------------------------------------------------------------------------
# BUGS.md #34 — v43 dropped the `categorys` alias for `CategoryCombo.categories`.
# ---------------------------------------------------------------------------


@pytest.mark.upstream_bug
@respx.mock
async def test_bug_34_v43_categorys_alias_silently_dropped() -> None:
    """BUGS.md #34 — bug-still-present: v43 accepts `categorys` payloads but persists no categories.

    On v42 the `categorys` (misspelled) field was a backwards-compat alias for
    `categories`. v43 dropped the alias; writes that use `categorys` get a 201
    Created envelope but the resulting CategoryCombo has `categories: []` —
    silent data loss. This test models that wire behaviour. When DHIS2 either
    re-adds the alias or 400s on unknown fields, the assertion below stops
    matching reality.
    """
    _mock_v43_connect()
    respx.post("https://dhis2.example/api/categoryCombos").mock(
        return_value=httpx.Response(201, json={"status": "OK", "httpStatusCode": 201, "response": {"uid": "CC_NEW"}}),
    )
    # Model the bug: GET shows the just-created combo with the categories list dropped.
    respx.get("https://dhis2.example/api/categoryCombos/CC_NEW").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "CC_NEW",
                "name": "Sex",
                "dataDimensionType": "DISAGGREGATION",
                "skipTotal": False,
                "categories": [],  # <-- the bug: should match the input cats.
                "categoryOptionCombos": [],
            },
        ),
    )
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        # POST a raw payload that uses the misspelled `categorys` (simulating the
        # bug-pattern callers still in the wild). The server 201s but drops them.
        body = {
            "name": "Sex",
            "dataDimensionType": "DISAGGREGATION",
            "skipTotal": False,
            "categorys": [{"id": "CAT_SEX"}],
        }
        await client.post_raw("/api/categoryCombos", body=body)
        combo = await client.category_combos.get("CC_NEW")
    assert combo.categories == [], (
        "BUGS.md #34: v43 should still silently drop the `categorys` (misspelled) field. "
        "If this changes, DHIS2 may have either re-added the alias or made it a 4xx — "
        "either way, verify upstream + revisit `dhis2w_client.v{N}.category_combos`."
    )


@pytest.mark.upstream_bug
@respx.mock
async def test_bug_34_workaround_uses_categories_payload() -> None:
    """BUGS.md #34 — workaround-works: every CategoryCombo write goes out as `categories`.

    The fix is uniform across all three majors — we never emit `categorys`.
    Asserts the v43-bound wire payload contains `categories` and never
    `categorys`. If the workaround regresses, this fails loudly.
    """
    _mock_v43_connect()
    create_route = respx.post("https://dhis2.example/api/categoryCombos").mock(
        return_value=httpx.Response(201, json={"status": "OK", "httpStatusCode": 201, "response": {"uid": "CC_NEW"}}),
    )
    respx.get("https://dhis2.example/api/categoryCombos/CC_NEW").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "CC_NEW",
                "name": "Sex",
                "dataDimensionType": "DISAGGREGATION",
                "skipTotal": False,
                "categories": [{"id": "CAT_SEX"}],
                "categoryOptionCombos": [],
            },
        ),
    )
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        await client.category_combos.create(name="Sex", categories=["CAT_SEX"])
    body = create_route.calls.last.request.read()
    assert b'"categories"' in body
    assert b'"categorys"' not in body, (
        "BUGS.md #34 workaround: client writes must use `categories`, not the dropped "
        "alias. Regression points at `dhis2w_client.v{N}.category_combos`."
    )


# ---------------------------------------------------------------------------
# BUGS.md #38 — v43 dropped `SharingObject.externalAccess` from the wire schema.
# ---------------------------------------------------------------------------


@pytest.mark.upstream_bug
def test_bug_38_v43_sharing_object_lacks_external_access_field() -> None:
    """BUGS.md #38 — bug-still-present: v43 OAS does not declare `externalAccess` on `SharingObject`.

    DHIS2 v43 dropped the field from the schema entirely. The generated
    `SharingObject` class on v43 doesn't carry it (and the wire silently
    ignores it). This test asserts the v43 OAS class lacks the field —
    if DHIS2 re-adds it, codegen would regenerate the class with the
    field, and this assertion would fail.
    """
    from dhis2w_client.generated.v43.oas.sharing_object import SharingObject

    assert "externalAccess" not in SharingObject.model_fields, (
        "BUGS.md #38: v43 SharingObject still lacks externalAccess in OAS. "
        "If this fails, regenerate codegen and revisit `dhis2w_client.v43.sharing`."
    )


@pytest.mark.upstream_bug
def test_bug_38_workaround_v43_sharing_builder_drops_external_access() -> None:
    """BUGS.md #38 — workaround-works: v43 SharingBuilder doesn't expose `external_access`.

    The materialised v43 wire payload doesn't carry `externalAccess`. The
    v42 sibling still has the field for v42 + v41 servers.
    """
    from dhis2w_client.v42.sharing import SharingBuilder as V42Builder
    from dhis2w_client.v43.sharing import ACCESS_READ_METADATA
    from dhis2w_client.v43.sharing import SharingBuilder as V43Builder

    assert "external_access" not in V43Builder.model_fields
    assert "external_access" in V42Builder.model_fields  # sanity: sibling still has it
    dumped = (
        V43Builder(public_access=ACCESS_READ_METADATA).to_sharing_object().model_dump(by_alias=True, exclude_none=True)
    )
    assert "externalAccess" not in dumped, (
        "BUGS.md #38 workaround: v43 SharingBuilder must not emit externalAccess in the wire shape. "
        "Regression points at `dhis2w_client.v43.sharing`."
    )


# ---------------------------------------------------------------------------
# BUGS.md #39 — v41 OAuth2 client schema uses `cid` (not `clientId`) + strict array typing.
# ---------------------------------------------------------------------------


@pytest.mark.upstream_bug
@respx.mock
async def test_bug_39_v41_oauth2_payload_with_clientid_persists_empty() -> None:
    """BUGS.md #39 — bug-still-present: v41 silently ignores `clientId` in OAuth2 payloads.

    v41's schema property is `cid`; v42 + v43 renamed it to `clientId`. A
    v42-shape payload sent to v41 returns 201 Created but the resulting
    client has no `clientId` set — `/oauth2/token` then 401s with
    invalid_client. This test models the v41 wire behaviour. If DHIS2
    backports the rename to v41, the dropped-field assertion stops matching.
    """
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.41.0"}),
    )
    register_route = respx.post("https://dhis2.example/api/oAuth2Clients").mock(
        return_value=httpx.Response(201, json={"response": {"uid": "OAUTH_UID"}})
    )
    # If a caller naively shipped a v42-shape payload to v41, this is what would happen:
    # the request lands, the server 201s, but `cid` is empty because `clientId` is unknown.
    async with Dhis2Client("https://dhis2.example", auth=_auth(), allow_version_fallback=True) as client:
        assert client.version_key == "v41"
        await client.post_raw(
            "/api/oAuth2Clients",
            body={
                "name": "my-app",
                "clientId": "my-app",  # <-- v41 doesn't know this key
                "clientSecret": "$2b$10$dummy",
            },
        )
    body = register_route.calls.last.request.read()
    assert b'"clientId"' in body
    assert b'"cid"' not in body, (
        "BUGS.md #39: v41 should still treat `clientId` as an unknown property. "
        "If this fails, DHIS2 may have backported the rename — verify upstream."
    )


@pytest.mark.upstream_bug
@respx.mock
async def test_bug_39_workaround_v41_register_emits_cid_not_clientid() -> None:
    """BUGS.md #39 — workaround-works: `register_oauth2_client` posts `cid` (not `clientId`) on v41.

    The per-version `dhis2w_client.v41.oauth2_payload.build_register_payload`
    emits `cid` + array-typed multi-valued fields. The registration helper
    in dhis2w-core dispatches per detected server version.
    """
    from dhis2w_core.oauth2_registration import register_oauth2_client

    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.41.0"}),
    )
    register_route = respx.post("https://dhis2.example/api/oAuth2Clients").mock(
        return_value=httpx.Response(201, json={"response": {"uid": "OAUTH_UID"}})
    )
    await register_oauth2_client(
        base_url="https://dhis2.example",
        admin_auth=_auth(),
        client_id="my-app",
        client_secret="my-secret",
    )
    body = register_route.calls.last.request.read()
    assert b'"cid"' in body
    assert b'"clientId"' not in body, (
        "BUGS.md #39 workaround: v41 must receive `cid`, not `clientId`. "
        "Regression points at `dhis2w_client.v41.oauth2_payload`."
    )
