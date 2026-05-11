"""Paired upstream-bug regression tests — one bug + one workaround per BUGS.md entry.

Every test here is marked `@pytest.mark.upstream_bug` and comes in two flavours:

- **Mocked (fast, default)** — respx-mocked tests that model the buggy
  wire shape and verify our workaround code handles it. Run by default
  via `make test`. These document the bug pattern but don't auto-detect
  upstream fixes.
- **Live (slow, opt-in)** — `@pytest.mark.slow` tests that hit the local
  docker DHIS2 stack (`make dhis2-run DHIS2_VERSION=N`) and verify the
  bug is still present on the actual wire. When DHIS2 ships an upstream
  fix, these fail loudly — the signal to drop the workaround. Each live
  test skips unless `client.version_key` matches the bug's target major,
  so you exercise v43 bugs against a v43 stack, v41 bugs against a v41
  stack, etc. Run all of them with `make test-slow` or just this suite
  with `make test-upstream-bugs -m slow`.

The marker is registered in `pyproject.toml`. List the regression
suite with `make test-upstream-bugs`. The full test suite (`make test`)
includes the mocked halves by default since they're fast.
"""

from __future__ import annotations

import os

import httpx
import pytest
import respx
from dhis2w_client import BasicAuth, Dhis2Client


def _auth() -> BasicAuth:
    """Throwaway BasicAuth for in-process respx tests."""
    return BasicAuth(username="admin", password="district")


def _live_auth() -> BasicAuth:
    """Admin basic auth for the local docker stack (seeded by `make dhis2-run`)."""
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


def _skip_if_stack_unreachable(url: str) -> None:
    """Skip the test when the local docker stack isn't responding to root probes."""
    try:
        with httpx.Client(timeout=2.0) as probe:
            probe.get(f"{url}/dhis-web-login/")
    except (httpx.RequestError, httpx.HTTPError) as exc:
        pytest.skip(f"local DHIS2 stack not reachable at {url} ({exc}). Run `make dhis2-run DHIS2_VERSION=<N>` first.")


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


# ---------------------------------------------------------------------------
# Live bug re-verification — opt-in via @pytest.mark.slow.
#
# These tests hit the local docker DHIS2 stack (`make dhis2-run
# DHIS2_VERSION=N`). Each one skips unless the connected server matches
# the bug's target major, so you don't need all three stacks running at
# once. When DHIS2 ships an upstream fix, the bug-still-present assertion
# starts failing — that's the loud signal to drop the workaround.
# ---------------------------------------------------------------------------


_AnyVersion = frozenset({"v41", "v42", "v43"})


def _skip_unless_version(client: Dhis2Client, targets: str | frozenset[str]) -> None:
    """Skip the test unless `client.version_key` is in the bug's target version set.

    When DHIS2 fixes a bug upstream, it usually lands on the latest major
    first while older majors keep the bug — so each verifier declares the
    set of versions it applies to. The default `_AnyVersion` covers
    cross-version bugs (the bug exists on every supported major); specific
    sets like `frozenset({"v43"})` scope to one major.
    """
    target_set = frozenset({targets}) if isinstance(targets, str) else targets
    if client.version_key not in target_set:
        pytest.skip(
            f"BUGS live test targets {sorted(target_set)}; connected to {client.version_key!r}. "
            f"Run `make dhis2-run DHIS2_VERSION=<N>` against one of the target majors first."
        )


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_33_v43_live_save_returns_empty_coc_matrix(local_url: str) -> None:
    """BUGS.md #33 — bug-still-present (LIVE v43): real save leaves COC matrix empty.

    Requires `make dhis2-run DHIS2_VERSION=43`. Creates a CategoryCombo over
    an existing seeded Category, GETs the just-created combo, asserts the
    `categoryOptionCombos` list is empty (the bug). Cleans up afterwards.
    If DHIS2 fixes the bug upstream, the assertion fails — verify upstream,
    then drop the workaround in `dhis2w_client/v43/category_combos.py`.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth()) as client:
        _skip_unless_version(client, "v43")
        cats = await client.get_raw("/api/categories", params={"fields": "id", "pageSize": "1"})
        rows = cats.get("categories") or []
        if not rows:
            pytest.skip("seeded fixture has no Categories — fresh stack?")
        cat_uid = rows[0]["id"]
        create_envelope = await client.post_raw(
            "/api/categoryCombos",
            body={
                "name": "BUGS_33_LIVE_TEST",
                "dataDimensionType": "DISAGGREGATION",
                "skipTotal": False,
                "categories": [{"id": cat_uid}],
            },
        )
        combo_uid = (create_envelope.get("response") or {}).get("uid")
        assert isinstance(combo_uid, str), f"unexpected create response: {create_envelope}"
        try:
            after = await client.get_raw(
                f"/api/categoryCombos/{combo_uid}",
                params={"fields": "id,categoryOptionCombos[id]"},
            )
            cocs = after.get("categoryOptionCombos") or []
            assert cocs == [], (
                f"BUGS.md #33: expected empty categoryOptionCombos on v43 save (bug-still-present), "
                f"got {len(cocs)} rows. DHIS2 may have shipped a fix — verify upstream, then drop "
                f"the workaround in `dhis2w_client/v43/category_combos.py`."
            )
        finally:
            await client.delete_raw(f"/api/categoryCombos/{combo_uid}")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_34_v43_live_categorys_alias_silently_dropped(local_url: str) -> None:
    """BUGS.md #34 — bug-still-present (LIVE v43): POST with `categorys` persists no categories.

    Requires `make dhis2-run DHIS2_VERSION=43`. POSTs a CategoryCombo using
    the misspelled `categorys` field. Reads back; asserts `categories: []`.
    If DHIS2 re-adds the alias (or starts 4xx-ing on unknown fields), the
    assertion fails.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth()) as client:
        _skip_unless_version(client, "v43")
        cats = await client.get_raw("/api/categories", params={"fields": "id", "pageSize": "1"})
        rows = cats.get("categories") or []
        if not rows:
            pytest.skip("seeded fixture has no Categories — fresh stack?")
        cat_uid = rows[0]["id"]
        create_envelope = await client.post_raw(
            "/api/categoryCombos",
            body={
                "name": "BUGS_34_LIVE_TEST",
                "dataDimensionType": "DISAGGREGATION",
                "skipTotal": False,
                "categorys": [{"id": cat_uid}],  # <-- the misspelled alias
            },
        )
        combo_uid = (create_envelope.get("response") or {}).get("uid")
        assert isinstance(combo_uid, str), f"unexpected create response: {create_envelope}"
        try:
            after = await client.get_raw(
                f"/api/categoryCombos/{combo_uid}",
                params={"fields": "id,categories[id]"},
            )
            categories = after.get("categories") or []
            assert categories == [], (
                f"BUGS.md #34: expected v43 to silently drop the `categorys` field, "
                f"got {len(categories)} categories on the persisted combo. DHIS2 may have "
                f"re-added the alias — verify upstream."
            )
        finally:
            await client.delete_raw(f"/api/categoryCombos/{combo_uid}")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_38_v43_live_sharing_schema_lacks_external_access(local_url: str) -> None:
    """BUGS.md #38 — bug-still-present (LIVE v43): `/api/schemas/sharingObject` does not list `externalAccess`.

    Requires `make dhis2-run DHIS2_VERSION=43`. Reads the schema directly
    from DHIS2 (no mutation needed) and asserts the field is absent. When
    DHIS2 re-adds it, the assertion fails.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth()) as client:
        _skip_unless_version(client, "v43")
        schema = await client.get_raw("/api/schemas/sharingObject", params={"fields": "properties[fieldName]"})
        field_names = {prop.get("fieldName") for prop in schema.get("properties") or []}
        assert "externalAccess" not in field_names, (
            "BUGS.md #38: expected v43 SharingObject schema to lack `externalAccess`. "
            "DHIS2 may have re-added the field — regenerate codegen and revisit "
            "`dhis2w_client.v43.sharing`."
        )


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_39_v41_live_oauth2_clientid_persists_empty(local_url: str) -> None:
    """BUGS.md #39 — bug-still-present (LIVE v41): POST with `clientId` persists with empty `cid`.

    Requires `make dhis2-run DHIS2_VERSION=41`. POSTs a v42-shape OAuth2 client
    (using `clientId`, not `cid`) directly via raw POST. Asserts the persisted
    record has no `cid` value. Cleans up afterwards.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth(), allow_version_fallback=True) as client:
        _skip_unless_version(client, "v41")
        create_envelope = await client.post_raw(
            "/api/oAuth2Clients",
            body={
                "name": "BUGS_39_LIVE_TEST",
                "clientId": "bugs-39-live-test",  # <-- v41 doesn't know this key
                "clientSecret": "$2b$10$dummy.bcrypt.hash.for.bug.test.only.not.used",
                "clientAuthenticationMethods": ["client_secret_basic"],
                "authorizationGrantTypes": ["authorization_code"],
                "redirectUris": ["http://localhost:8765"],
                "scopes": ["ALL"],
            },
        )
        uid = (create_envelope.get("response") or {}).get("uid")
        assert isinstance(uid, str), f"unexpected create response: {create_envelope}"
        try:
            after = await client.get_raw(
                f"/api/oAuth2Clients/{uid}",
                params={"fields": "id,cid,clientId"},
            )
            # On v41 the `clientId` we sent is silently dropped; `cid` stays empty.
            cid = after.get("cid")
            assert not cid, (
                f"BUGS.md #39: expected v41 to silently drop `clientId` (cid stays empty), "
                f"got cid={cid!r}. DHIS2 may have backported the rename — verify upstream."
            )
        finally:
            await client.delete_raw(f"/api/oAuth2Clients/{uid}")


# ---------------------------------------------------------------------------
# Backlog — every BUGS.md entry deserves a live verifier; fill in incrementally.
# ---------------------------------------------------------------------------


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_1_live_verifier(local_url: str) -> None:
    """BUGS.md #1 — `/api/analytics/rawData` returns 404 without the `.json` URL suffix.

    Cross-version bug (v41/v42/v43): the sub-routes under `/api/analytics`
    only honour extension-suffixed paths. With `Accept: application/json`
    but no extension, Tomcat 404s. With `.json` appended the same query
    returns 200.

    Workaround: `dhis2w_core.plugins.analytics.service` hardcodes `.json`
    on every sub-route URL.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth(), allow_version_fallback=True) as client:
        _skip_unless_version(client, _AnyVersion)
        without_ext = await client._request(  # noqa: SLF001 — direct probe, not a parsed call
            "GET",
            "/api/analytics/rawData",
            params={"dimension": "dx:nonexistent", "skipMeta": "true"},
            extra_headers={"Accept": "application/json"},
        )
        with_ext = await client._request(  # noqa: SLF001
            "GET",
            "/api/analytics/rawData.json",
            params={"dimension": "dx:nonexistent", "skipMeta": "true"},
            extra_headers={"Accept": "application/json"},
        )
    assert without_ext.status_code == 404, (
        f"BUGS.md #1: expected 404 on `/api/analytics/rawData` without `.json` "
        f"(Tomcat 'no static resource' fall-through), got {without_ext.status_code}. "
        f"DHIS2 may have fixed content-negotiation on the sub-route — verify upstream + "
        f"drop the `.json`-hardcode in `dhis2w_core.plugins.analytics.service`."
    )
    assert with_ext.status_code != 404, (
        f"BUGS.md #1: expected `.json`-suffixed call to NOT be 404 (the workaround relies "
        f"on the suffix making the route resolve), got {with_ext.status_code}."
    )


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_2_live_verifier(local_url: str) -> None:
    """BUGS.md #2 — TODO live verifier: `importStrategy=DELETE` on `/api/dataValueSets` is a soft-delete that still b...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #2 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #2")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_3_live_verifier(local_url: str) -> None:
    """BUGS.md #3 — TODO live verifier: Blank `audit.metadata` / `audit.tracker` / `audit.aggregate` in `dhis.conf` s...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #3 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #3")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_4_live_verifier(local_url: str) -> None:
    """BUGS.md #4 — TODO live verifier: DHIS2 OAuth2 Authorization Server requires 10+ undocumented `dhis.conf` keys...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #4 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #4")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_5_live_verifier(local_url: str) -> None:
    """BUGS.md #5 — TODO live verifier: `organisationUnits` POST inside a user's capture scope enforces DESCENDANT, n...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #5 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #5")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_6_live_verifier(local_url: str) -> None:
    """BUGS.md #6 — TODO live verifier: Bulk `/api/dataValueSets` push returns 409 even when every row's `ignored`, h...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #6 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #6")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_7_live_verifier(local_url: str) -> None:
    """BUGS.md #7 — TODO live verifier: DHIS2's OpenAPI names the primary key `uid` while the REST API wire format us...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #7 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #7")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_8_live_verifier(local_url: str) -> None:
    """BUGS.md #8 — `/api/schemas/userRole.properties.authorities.fieldName` is `"authoritys"`.

    Cross-version bug (v41/v42/v43): DHIS2's auto-pluralizer mangles
    `authority` -> `authoritys` for the `UserRole.authorities` property's
    wire fieldName. The wire still accepts `authorities`, but anything
    that walks the schema and uses fieldName as-is breaks.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth(), allow_version_fallback=True) as client:
        _skip_unless_version(client, _AnyVersion)
        schema = await client.get_raw("/api/schemas/userRole", params={"fields": "properties[name,fieldName]"})
        authorities = next(
            (p for p in schema.get("properties") or [] if p.get("name") == "authorities"),
            None,
        )
    assert authorities is not None, "BUGS.md #8: expected to find a `authorities` property on UserRole schema."
    assert authorities.get("fieldName") == "authoritys", (
        f"BUGS.md #8: expected fieldName==`authoritys` (the misspelling), got {authorities.get('fieldName')!r}. "
        f"DHIS2 may have fixed the auto-pluralizer — verify upstream + drop the alias workaround."
    )


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_9_live_verifier(local_url: str) -> None:
    """BUGS.md #9 — TODO live verifier: DHIS2's strict OIDC property parser rejects entire provider config on typos

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #9 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #9")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_10_live_verifier(local_url: str) -> None:
    """BUGS.md #10 — TODO live verifier: Login-page system-setting keys are a mix of prefixed and unprefixed

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #10 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #10")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_11_live_verifier(local_url: str) -> None:
    """BUGS.md #11 — TODO live verifier: `POST /api/staticContent/logo_front` succeeds but DHIS2 keeps serving the bu...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #11 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #11")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_12_live_verifier(local_url: str) -> None:
    """BUGS.md #12 — TODO live verifier: DHIS2 login app leaves `html` transparent, so browser zoom > 100% exposes th...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #12 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #12")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_13_live_verifier(local_url: str) -> None:
    """BUGS.md #13 — TODO live verifier: `OutlierDetectionAlgorithm` OAS enum reports `MOD_Z_SCORE` but DHIS2 rejects...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #13 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #13")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_14_live_verifier(local_url: str) -> None:
    """BUGS.md #14 — Route auth-scheme schemas in OAS lack a `type` discriminator.

    Cross-version bug (v41/v42/v43; v41 doesn't even have the
    `oauth2-client-credentials` variant — see BUGS.md #39). The
    HttpBasicAuthScheme / ApiTokenAuthScheme / ApiHeadersAuthScheme /
    ApiQueryParamsAuthScheme schemas in `/api/openapi.json` describe the
    same wire envelope without a `type` field that distinguishes them.
    The codegen spec-patch (`dhis2w_codegen.spec_patches`) synthesises the
    discriminator at build time. This test asserts the upstream OAS still
    omits the discriminator.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth(), allow_version_fallback=True) as client:
        _skip_unless_version(client, _AnyVersion)
        spec = await client.get_raw("/api/openapi.json")
    schemas = spec.get("components", {}).get("schemas", {}) or {}
    basic = schemas.get("HttpBasicAuthScheme") or {}
    props = basic.get("properties") or {}
    assert "type" not in props, (
        f"BUGS.md #14: expected HttpBasicAuthScheme to lack a `type` discriminator property, "
        f"got properties={sorted(props)}. DHIS2 may have added the discriminator — verify "
        f"upstream + drop the spec-patch in `dhis2w_codegen.spec_patches`."
    )


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_15_live_verifier(local_url: str) -> None:
    """BUGS.md #15 — TODO live verifier: OAS emits `JobConfiguration.jobParameters` and `WebMessage.response` as undi...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #15 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #15")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_16_live_verifier(local_url: str) -> None:
    """BUGS.md #16 — TODO live verifier: `POST /api/documents` rejects multipart uploads with 415, forcing a two-step...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #16 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #16")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_17_live_verifier(local_url: str) -> None:
    """BUGS.md #17 — TODO live verifier: `POST /api/messageConversations` returns the new UID on the `Location` heade...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #17 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #17")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_18_live_verifier(local_url: str) -> None:
    """BUGS.md #18 — TODO live verifier: `POST /api/messageConversations/{uid}` takes `text/plain` body; `send` requi...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #18 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #18")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_19_live_verifier(local_url: str) -> None:
    """BUGS.md #19 — TODO live verifier: `GET /api/validationResults` silently ignores `fields=*` and `fields=:all`

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #19 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #19")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_20_live_verifier(local_url: str) -> None:
    """BUGS.md #20 — TODO live verifier: `DELETE /api/options/{uid}` returns 200 OK but leaves the option in place

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #20 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #20")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_21_live_verifier(local_url: str) -> None:
    """BUGS.md #21 — TODO live verifier: Attribute-value filters: path property is the Attribute UID, not `attributeV...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #21 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #21")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_22_live_verifier(local_url: str) -> None:
    """BUGS.md #22 — TODO live verifier: `ProgramRuleVariable.sourceType` is a schema fiction — wire uses `programRul...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #22 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #22")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_23_live_verifier(local_url: str) -> None:
    """BUGS.md #23 — TODO live verifier: Single-pass `/api/metadata` with DataSets + dependencies trips a Hibernate f...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #23 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #23")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_24_live_verifier(local_url: str) -> None:
    """BUGS.md #24 — TODO live verifier: Fresh install's built-in TET "Person" + TEAs "First name"/"Last name" collid...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #24 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #24")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_25_live_verifier(local_url: str) -> None:
    """BUGS.md #25 — TODO live verifier: `/api/.../metadata` leaks computed fields that confuse re-imports

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #25 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #25")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_26_live_verifier(local_url: str) -> None:
    """BUGS.md #26 — TODO live verifier: Admin OU scope is cached per session — scope changes need a re-login

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #26 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #26")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_27_live_verifier(local_url: str) -> None:
    """BUGS.md #27 — TODO live verifier: Fresh DHIS2 installs are flaky during first metadata import

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #27 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #27")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_28_live_verifier(local_url: str) -> None:
    """BUGS.md #28 — `RelativePeriods` OAS schema is 45 booleans, not an enum.

    Cross-version bug. Codegen-shape decision DHIS2's `/api/openapi.json`
    has been doing for years. `RelativePeriods` enumerates every relative
    period (`last12Months`, `thisYear`, ...) as a boolean property instead
    of a single enum with a literal value set.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth(), allow_version_fallback=True) as client:
        _skip_unless_version(client, _AnyVersion)
        spec = await client.get_raw("/api/openapi.json")
    rel = spec.get("components", {}).get("schemas", {}).get("RelativePeriods") or {}
    props = rel.get("properties") or {}
    boolean_props = [name for name, body in props.items() if (body or {}).get("type") == "boolean"]
    assert len(boolean_props) >= 30, (
        f"BUGS.md #28: expected RelativePeriods to carry many boolean properties (got "
        f"{len(boolean_props)}). If DHIS2 reshaped it as a single enum, this test is "
        f"the loud signal to revisit `dhis2w_client.v{{N}}.helpers.viz` + drop "
        f"`RelativePeriod` shim."
    )


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_29_live_verifier(local_url: str) -> None:
    """BUGS.md #29 — `/api/metadata?filter=...&rootJunction=OR` silently ANDs multiple filters.

    Cross-version bug. DHIS2 advertises `rootJunction` for cross-filter
    boolean logic but the metadata endpoint ignores the parameter and
    always ANDs. This verifier asks for indicators matching either of
    two mutually exclusive UID conditions — bug-present means the
    response is empty; bug-fixed means at least one row comes back.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth(), allow_version_fallback=True) as client:
        _skip_unless_version(client, _AnyVersion)
        # Pick two UIDs that won't match together (an indicator can't have
        # both UIDs at once), so AND => empty, OR => at least one match.
        sample = await client.get_raw(
            "/api/indicators",
            params={"fields": "id", "pageSize": "2"},
        )
        indicators = sample.get("indicators") or []
        if len(indicators) < 2:
            pytest.skip("seeded fixture has fewer than 2 indicators")
        uid_a = indicators[0]["id"]
        uid_b = indicators[1]["id"]
        with_or = await client.get_raw(
            "/api/metadata",
            params={
                "filter": [f"indicators:id:eq:{uid_a}", f"indicators:id:eq:{uid_b}"],
                "rootJunction": "OR",
                "fields": "indicators[id]",
            },
        )
    indicator_rows = with_or.get("indicators") or []
    assert indicator_rows == [], (
        f"BUGS.md #29: expected rootJunction=OR with conflicting filters to still AND on "
        f"v41/v42/v43 (empty result). Got {len(indicator_rows)} rows — DHIS2 may have wired "
        f"up rootJunction properly. Verify upstream + drop the per-filter fanout workaround "
        f"in `dhis2w_client.v{{N}}.metadata.search`."
    )


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_30_live_verifier(local_url: str) -> None:
    """BUGS.md #30 — `/api/appHub` returns `versions[*].created` as epoch-millis integers.

    Cross-version bug. DHIS2 proxies App Hub responses and converts ISO-8601
    timestamps into epoch-millis integers. Any parser that expects strings
    blows up. Workaround at `dhis2w_client.v{N}.apps` normalises the field
    to an integer-or-string union and parses both shapes.
    """
    _skip_if_stack_unreachable(local_url)
    async with Dhis2Client(local_url, auth=_live_auth(), allow_version_fallback=True) as client:
        _skip_unless_version(client, _AnyVersion)
        try:
            hub = await client.get_raw("/api/appHub")
        except Exception as exc:  # noqa: BLE001 — App Hub needs internet egress
            pytest.skip(f"App Hub not reachable from this stack ({exc})")
    apps_raw = hub if isinstance(hub, list) else (hub.get("appHub") or [])
    apps: list[dict[str, object]] = list(apps_raw) if isinstance(apps_raw, list) else []
    if not apps:
        pytest.skip("App Hub returned no apps (no internet egress?)")
    first_app: dict[str, object] = apps[0]
    versions_raw = first_app.get("versions") or []
    versions: list[dict[str, object]] = list(versions_raw) if isinstance(versions_raw, list) else []
    if not versions:
        pytest.skip("first App Hub app has no versions")
    created = versions[0].get("created")
    assert isinstance(created, int), (
        f"BUGS.md #30: expected `versions[0].created` to be an epoch-millis int, got "
        f"{type(created).__name__}({created!r}). DHIS2 may have fixed the proxy "
        f"normalisation — verify upstream + relax the union type in "
        f"`dhis2w_client.v{{N}}.apps`."
    )


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_31_live_verifier(local_url: str) -> None:
    """BUGS.md #31 — TODO live verifier: Predictor expression parser rejects uppercase aggregators (`AVG()` / `SUM()`)

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #31 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #31")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_32_live_verifier(local_url: str) -> None:
    """BUGS.md #32 — TODO live verifier: `POST /api/systemSettings/keyCalendar` returns 200 OK but the value never pe...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #32 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #32")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_35_live_verifier(local_url: str) -> None:
    """BUGS.md #35 — TODO live verifier: v43: `POST /api/dataValueSets` aborts the whole chunk when a DE belongs to m...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #35 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #35")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_36_live_verifier(local_url: str) -> None:
    """BUGS.md #36 — TODO live verifier: v43: building event analytics for an event-program with 2024 data fails with...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #36 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #36")


@pytest.mark.upstream_bug
@pytest.mark.slow
async def test_bug_37_live_verifier(local_url: str) -> None:
    """BUGS.md #37 — TODO live verifier: v43: fresh `POST /api/dataValueSets` CREATE is ~80x slower per row than v41...

    Placeholder. Fill in the live wire check that asserts the bug is
    still observable on a real DHIS2 stack. When DHIS2 ships a fix, the
    assertion fails — the loud signal we can drop the workaround.

    See BUGS.md #37 for the curl repro + the workaround pointer.
    """
    _skip_if_stack_unreachable(local_url)
    pytest.skip("TODO: implement live verifier — see BUGS.md #37")
