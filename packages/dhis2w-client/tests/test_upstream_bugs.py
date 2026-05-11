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
