"""Unit tests for `Dhis2Client.categories` — respx-mocked."""

from __future__ import annotations

import json as _json

import httpx
import pytest
import respx
from dhis2_client import BasicAuth, Category, Dhis2Client


def _auth() -> BasicAuth:
    return BasicAuth(username="admin", password="district")


def _mock_preamble() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.0"}),
    )


@respx.mock
async def test_list_all_returns_typed_categories() -> None:
    _mock_preamble()
    respx.get("https://dhis2.example/api/categories").mock(
        return_value=httpx.Response(
            200,
            json={
                "categories": [
                    {
                        "id": "CAT_SEX",
                        "name": "Sex",
                        "shortName": "Sex",
                        "dataDimensionType": "DISAGGREGATION",
                        "categoryOptions": [
                            {"id": "CO_M", "name": "Male"},
                            {"id": "CO_F", "name": "Female"},
                        ],
                    },
                ],
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        rows = await client.categories.list_all()
    finally:
        await client.close()
    assert len(rows) == 1
    assert isinstance(rows[0], Category)
    assert rows[0].id == "CAT_SEX"
    assert rows[0].dataDimensionType == "DISAGGREGATION"


@respx.mock
async def test_create_wires_options_in_payload_and_fetches_back() -> None:
    _mock_preamble()
    create_route = respx.post("https://dhis2.example/api/categories").mock(
        return_value=httpx.Response(
            201,
            json={"status": "OK", "httpStatusCode": 201, "response": {"uid": "CAT_NEW"}},
        ),
    )
    respx.get("https://dhis2.example/api/categories/CAT_NEW").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "CAT_NEW",
                "name": "Modality",
                "shortName": "Mod",
                "dataDimensionType": "DISAGGREGATION",
                "categoryOptions": [{"id": "CO_X"}, {"id": "CO_Y"}],
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        created = await client.categories.create(
            name="Modality",
            short_name="Mod",
            options=["CO_X", "CO_Y"],
        )
    finally:
        await client.close()
    body = _json.loads(create_route.calls.last.request.read())
    assert body["name"] == "Modality"
    assert body["dataDimensionType"] == "DISAGGREGATION"
    assert body["categoryOptions"] == [{"id": "CO_X"}, {"id": "CO_Y"}]
    assert created.id == "CAT_NEW"


@respx.mock
async def test_rename_partial_updates_only_the_passed_fields() -> None:
    _mock_preamble()
    respx.get("https://dhis2.example/api/categories/CAT_A").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "CAT_A",
                "name": "Sex",
                "shortName": "Sex",
                "code": "SEX",
                "description": "Original",
                "dataDimensionType": "DISAGGREGATION",
            },
        ),
    )
    put_route = respx.put("https://dhis2.example/api/categories/CAT_A").mock(
        return_value=httpx.Response(200, json={}),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.categories.rename("CAT_A", short_name="Gender")
    finally:
        await client.close()
    body = _json.loads(put_route.calls.last.request.read())
    assert body["shortName"] == "Gender"
    assert body["name"] == "Sex"  # untouched
    assert body["description"] == "Original"  # untouched


async def test_rename_rejects_no_op_call() -> None:
    """Service layer surfaces a ValueError when no rename field was passed."""
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    with pytest.raises(ValueError, match="rename requires"):
        await client.categories.rename("CAT_A")
