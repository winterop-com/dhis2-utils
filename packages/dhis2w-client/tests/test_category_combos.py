"""Unit tests for `Dhis2Client.category_combos` + `category_option_combos` — respx-mocked."""

from __future__ import annotations

import json as _json

import httpx
import pytest
import respx
from dhis2w_client import (
    BasicAuth,
    CategoryCombo,
    CategoryOptionCombo,
    Dhis2Client,
)


def _auth() -> BasicAuth:
    return BasicAuth(username="admin", password="district")


def _mock_preamble() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.0"}),
    )


@respx.mock
async def test_combo_list_all_returns_typed_combos() -> None:
    _mock_preamble()
    respx.get("https://dhis2.example/api/categoryCombos").mock(
        return_value=httpx.Response(
            200,
            json={
                "categoryCombos": [
                    {
                        "id": "CC_DEFAULT",
                        "name": "default",
                        "isDefault": True,
                        "dataDimensionType": "DISAGGREGATION",
                        "categorys": [{"id": "CAT_DEFAULT"}],
                        "categoryOptionCombos": [{"id": "COC_DEFAULT"}],
                    },
                ],
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        rows = await client.category_combos.list_all()
    finally:
        await client.close()
    assert len(rows) == 1
    assert isinstance(rows[0], CategoryCombo)
    assert rows[0].isDefault is True


@respx.mock
async def test_combo_create_wires_categories_in_payload() -> None:
    _mock_preamble()
    create_route = respx.post("https://dhis2.example/api/categoryCombos").mock(
        return_value=httpx.Response(
            201,
            json={"status": "OK", "httpStatusCode": 201, "response": {"uid": "CC_NEW"}},
        ),
    )
    respx.get("https://dhis2.example/api/categoryCombos/CC_NEW").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "CC_NEW",
                "name": "Sex x AgeGroup",
                "dataDimensionType": "DISAGGREGATION",
                "skipTotal": False,
                "categorys": [{"id": "CAT_SEX"}, {"id": "CAT_AGE"}],
                "categoryOptionCombos": [],
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        created = await client.category_combos.create(
            name="Sex x AgeGroup",
            categories=["CAT_SEX", "CAT_AGE"],
        )
    finally:
        await client.close()
    body = _json.loads(create_route.calls.last.request.read())
    assert body["name"] == "Sex x AgeGroup"
    assert body["dataDimensionType"] == "DISAGGREGATION"
    assert body["categorys"] == [{"id": "CAT_SEX"}, {"id": "CAT_AGE"}]
    assert body["skipTotal"] is False
    assert created.id == "CC_NEW"


async def test_combo_create_rejects_empty_categories() -> None:
    """A CategoryCombo with no Categories is invalid — service surfaces ValueError."""
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    with pytest.raises(ValueError, match="at least one category"):
        await client.category_combos.create(name="Empty", categories=[])


@respx.mock
async def test_combo_wait_for_coc_generation_returns_when_count_lands() -> None:
    """Helper polls until CategoryOptionCombo count reaches `expected_count`."""
    _mock_preamble()
    response_sequence = [
        httpx.Response(200, json={"categoryOptionCombos": [{"id": "COC_1"}]}),
        httpx.Response(200, json={"categoryOptionCombos": [{"id": "COC_1"}, {"id": "COC_2"}]}),
        httpx.Response(
            200,
            json={"categoryOptionCombos": [{"id": "COC_1"}, {"id": "COC_2"}, {"id": "COC_3"}, {"id": "COC_4"}]},
        ),
    ]
    respx.get("https://dhis2.example/api/categoryOptionCombos").mock(side_effect=response_sequence)
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        landed = await client.category_combos.wait_for_coc_generation(
            "CC_BIG", expected_count=4, timeout_seconds=5.0, poll_interval_seconds=0.01
        )
    finally:
        await client.close()
    assert landed == 4


@respx.mock
async def test_combo_wait_for_coc_generation_times_out() -> None:
    _mock_preamble()
    respx.get("https://dhis2.example/api/categoryOptionCombos").mock(
        return_value=httpx.Response(200, json={"categoryOptionCombos": [{"id": "COC_1"}]}),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        with pytest.raises(TimeoutError, match="expected 4"):
            await client.category_combos.wait_for_coc_generation(
                "CC_STALE", expected_count=4, timeout_seconds=0.05, poll_interval_seconds=0.01
            )
    finally:
        await client.close()


@respx.mock
async def test_coc_list_for_combo_filters_by_category_combo_id() -> None:
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/categoryOptionCombos").mock(
        return_value=httpx.Response(
            200,
            json={
                "categoryOptionCombos": [
                    {"id": "COC_M", "name": "Male", "categoryCombo": {"id": "CC_SEX"}},
                    {"id": "COC_F", "name": "Female", "categoryCombo": {"id": "CC_SEX"}},
                ]
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        rows = await client.category_option_combos.list_for_combo("CC_SEX")
    finally:
        await client.close()
    assert route.call_count == 1
    assert route.calls.last.request.url.params["filter"] == "categoryCombo.id:eq:CC_SEX"
    assert all(isinstance(row, CategoryOptionCombo) for row in rows)
    assert {row.id for row in rows} == {"COC_M", "COC_F"}
