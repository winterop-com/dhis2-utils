"""Unit tests for `OptionSetsAccessor` — respx-mocked, no live stack."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx
from dhis2_client import BasicAuth, Dhis2Client, OptionSpec


def _auth() -> BasicAuth:
    return BasicAuth(username="admin", password="district")


def _mock_preamble() -> None:
    """Mock the preamble `Dhis2Client.connect()` makes against DHIS2."""
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.0"}),
    )


@respx.mock
async def test_get_by_code_returns_none_when_no_match() -> None:
    """Empty `optionSets` list from DHIS2 maps to a None return — not an error."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/optionSets").mock(
        return_value=httpx.Response(200, json={"optionSets": []}),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.option_sets.get_by_code("MISSING_SET")
    finally:
        await client.close()
    assert result is None


@respx.mock
async def test_get_by_code_returns_typed_model_with_options() -> None:
    """Happy path: DHIS2 returns one match → typed `OptionSet` with options populated."""
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/optionSets").mock(
        return_value=httpx.Response(
            200,
            json={
                "optionSets": [
                    {
                        "id": "OsVaccType1",
                        "code": "VACCINE_TYPE",
                        "name": "Vaccine type",
                        "valueType": "TEXT",
                        "options": [
                            {"id": "OptVacBCG01", "code": "BCG", "name": "BCG", "sortOrder": 0},
                            {"id": "OptVacMes01", "code": "MEASLES", "name": "Measles", "sortOrder": 1},
                        ],
                    }
                ]
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.option_sets.get_by_code("VACCINE_TYPE")
    finally:
        await client.close()

    params = route.calls.last.request.url.params
    assert params["filter"] == "code:eq:VACCINE_TYPE"
    assert "options[id,code,name,sortOrder]" in params["fields"]
    assert result is not None
    assert result.id == "OsVaccType1"
    assert result.options is not None
    assert len(result.options) == 2


@respx.mock
async def test_list_options_orders_by_sort_order() -> None:
    """`list_options` hits /api/options with the right filter + order param."""
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/options").mock(
        return_value=httpx.Response(
            200,
            json={
                "options": [
                    {"id": "o1", "code": "BCG", "name": "BCG", "sortOrder": 0},
                    {"id": "o2", "code": "MEASLES", "name": "Measles", "sortOrder": 1},
                ]
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.option_sets.list_options("OsVaccType1")
    finally:
        await client.close()
    params = route.calls.last.request.url.params
    assert params["filter"] == "optionSet.id:eq:OsVaccType1"
    assert params["order"] == "sortOrder:asc"
    assert [o.code for o in result] == ["BCG", "MEASLES"]


@respx.mock
async def test_find_option_requires_exactly_one_selector() -> None:
    """Callers must pass one of code / name — never both, never neither."""
    _mock_preamble()
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        with pytest.raises(ValueError, match="exactly one"):
            await client.option_sets.find_option("OsVaccType1")
        with pytest.raises(ValueError, match="exactly one"):
            await client.option_sets.find_option("OsVaccType1", option_code="X", option_name="Y")
    finally:
        await client.close()


@respx.mock
async def test_find_option_filters_server_side_by_code() -> None:
    """`find_option` ships both filters (optionSet.id + code) as repeatable params."""
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/options").mock(
        return_value=httpx.Response(
            200,
            json={"options": [{"id": "o1", "code": "BCG", "name": "BCG", "sortOrder": 0}]},
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.option_sets.find_option("OsVaccType1", option_code="BCG")
    finally:
        await client.close()
    filters = route.calls.last.request.url.params.get_list("filter")
    assert "optionSet.id:eq:OsVaccType1" in filters
    assert "code:eq:BCG" in filters
    assert result is not None
    assert result.code == "BCG"


async def test_upsert_options_rejects_duplicate_codes_in_spec() -> None:
    """Pure-Python guard: passing two specs with the same code is a programming error."""
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    spec = [
        OptionSpec(code="BCG", name="BCG"),
        OptionSpec(code="BCG", name="BCG again"),
    ]
    with pytest.raises(ValueError, match="duplicate codes"):
        await client.option_sets.upsert_options("OsVaccType1", spec, dry_run=True)


@respx.mock
async def test_upsert_options_dry_run_reports_diff_without_writing() -> None:
    """Dry-run inspects current state but never POSTs / DELETEs."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/options").mock(
        return_value=httpx.Response(
            200,
            json={
                "options": [
                    {"id": "o_bcg", "code": "BCG", "name": "BCG", "sortOrder": 0},
                    {"id": "o_mes", "code": "MEASLES", "name": "Measles", "sortOrder": 1},
                    {"id": "o_pol", "code": "POLIO", "name": "Polio", "sortOrder": 2},
                ]
            },
        ),
    )
    write_route = respx.post("https://dhis2.example/api/metadata")

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        spec = [
            OptionSpec(code="BCG", name="BCG"),  # unchanged → skip
            OptionSpec(code="MEASLES", name="Measles vaccine"),  # name change → update
            OptionSpec(code="HPV", name="HPV vaccine"),  # new → add
        ]
        report = await client.option_sets.upsert_options(
            "OsVaccType1",
            spec,
            remove_missing=True,
            dry_run=True,
        )
    finally:
        await client.close()

    assert report.added == ["HPV"]
    assert report.updated == ["MEASLES"]
    assert report.skipped == ["BCG"]
    assert report.removed == ["POLIO"]  # current POLIO is missing from spec
    assert report.dry_run is True
    # Nothing was written — no /api/metadata calls fired.
    assert write_route.call_count == 0


@respx.mock
async def test_upsert_options_writes_and_deletes_via_metadata_bundle() -> None:
    """Real run uses `save_bulk` for writes + metadata bundle DELETE for removes (BUGS.md #20)."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/options").mock(
        return_value=httpx.Response(
            200,
            json={
                "options": [
                    {"id": "o_bcg", "code": "BCG", "name": "BCG", "sortOrder": 0},
                    {"id": "o_pol", "code": "POLIO", "name": "Polio", "sortOrder": 1},
                ]
            },
        ),
    )
    # Every POST /api/metadata (either save_bulk CREATE_AND_UPDATE or delete_bulk
    # DELETE) returns a success envelope; tests inspect which strategy was sent.
    posts: list[dict[str, Any]] = []

    def capture(request: httpx.Request) -> httpx.Response:
        posts.append(
            {
                "strategy": request.url.params.get("importStrategy"),
                "body": json.loads(request.content),
            },
        )
        return httpx.Response(200, json={"status": "OK", "stats": {"deleted": 1}})

    respx.post("https://dhis2.example/api/metadata").mock(side_effect=capture)

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        spec = [
            OptionSpec(code="BCG", name="BCG"),  # skip
            OptionSpec(code="HPV", name="HPV vaccine"),  # add
        ]
        report = await client.option_sets.upsert_options(
            "OsVaccType1",
            spec,
            remove_missing=True,
        )
    finally:
        await client.close()

    assert report.added == ["HPV"]
    assert report.removed == ["POLIO"]

    # Two POSTs: one save_bulk (CREATE_AND_UPDATE) for HPV, one delete_bulk
    # (DELETE) for POLIO.
    strategies = [p["strategy"] for p in posts]
    assert "CREATE_AND_UPDATE" in strategies
    assert "DELETE" in strategies
    delete_post = next(p for p in posts if p["strategy"] == "DELETE")
    deleted_uids = [entry["id"] for entry in delete_post["body"]["options"]]
    assert deleted_uids == ["o_pol"]
