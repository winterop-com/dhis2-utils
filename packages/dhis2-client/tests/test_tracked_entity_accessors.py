"""Unit tests for `TrackedEntityAttributesAccessor` + `TrackedEntityTypesAccessor` — respx-mocked."""

from __future__ import annotations

import json as _json
from typing import Any

import httpx
import respx
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.generated.v42.enums import ValueType


def _auth() -> BasicAuth:
    return BasicAuth(username="admin", password="district")


def _mock_preamble() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.0"}),
    )


# ---- TrackedEntityAttributesAccessor ---------------------------------------


@respx.mock
async def test_tea_list_all_filters_by_value_type() -> None:
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/trackedEntityAttributes").mock(
        return_value=httpx.Response(
            200,
            json={"trackedEntityAttributes": [{"id": "TEAnational1", "name": "National ID", "valueType": "TEXT"}]},
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        rows = await client.tracked_entity_attributes.list_all(value_type=ValueType.TEXT)
    finally:
        await client.close()
    assert route.calls.last.request.url.params["filter"] == "valueType:eq:TEXT"
    assert [r.id for r in rows] == ["TEAnational1"]


@respx.mock
async def test_tea_create_posts_payload_with_flags_and_option_set() -> None:
    _mock_preamble()
    post = respx.post("https://dhis2.example/api/trackedEntityAttributes").mock(
        return_value=httpx.Response(201, json={"response": {"uid": "TEA_NEW00001"}}),
    )
    respx.get("https://dhis2.example/api/trackedEntityAttributes/TEA_NEW00001").mock(
        return_value=httpx.Response(200, json={"id": "TEA_NEW00001", "name": "National ID"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        tea = await client.tracked_entity_attributes.create(
            name="National ID",
            short_name="NatID",
            value_type=ValueType.TEXT,
            unique=True,
            generated=True,
            pattern="#(ORGUNIT)(RANDOM)",
            option_set_uid="optSetGender1",
        )
    finally:
        await client.close()
    body: dict[str, Any] = _json.loads(post.calls.last.request.read())
    assert body["valueType"] == "TEXT"
    assert body["unique"] is True
    assert body["generated"] is True
    assert body["pattern"] == "#(ORGUNIT)(RANDOM)"
    assert body["optionSet"] == {"id": "optSetGender1"}
    assert tea.id == "TEA_NEW00001"


@respx.mock
async def test_tea_delete_routes_to_uid() -> None:
    _mock_preamble()
    route = respx.delete("https://dhis2.example/api/trackedEntityAttributes/TEA_X").mock(
        return_value=httpx.Response(204),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.tracked_entity_attributes.delete("TEA_X")
    finally:
        await client.close()
    assert route.called


# ---- TrackedEntityTypesAccessor --------------------------------------------


@respx.mock
async def test_tet_create_posts_payload() -> None:
    _mock_preamble()
    post = respx.post("https://dhis2.example/api/trackedEntityTypes").mock(
        return_value=httpx.Response(201, json={"response": {"uid": "TET_NEW00001"}}),
    )
    respx.get("https://dhis2.example/api/trackedEntityTypes/TET_NEW00001").mock(
        return_value=httpx.Response(200, json={"id": "TET_NEW00001", "name": "Person"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        tet = await client.tracked_entity_types.create(
            name="Person",
            short_name="Person",
            allow_audit_log=True,
            min_attributes_required_to_search=1,
        )
    finally:
        await client.close()
    body: dict[str, Any] = _json.loads(post.calls.last.request.read())
    assert body["name"] == "Person"
    assert body["allowAuditLog"] is True
    assert body["minAttributesRequiredToSearch"] == 1
    assert tet.id == "TET_NEW00001"


@respx.mock
async def test_tet_add_attribute_round_trips_and_strips_self_ref() -> None:
    _mock_preamble()
    respx.get("https://dhis2.example/api/trackedEntityTypes/TET1").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "TET1",
                "name": "Person",
                "trackedEntityTypeAttributes": [
                    {
                        "trackedEntityAttribute": {"id": "TEA_A"},
                        "mandatory": True,
                        "trackedEntityType": {"id": "TET1"},
                    },
                ],
            },
        ),
    )
    put = respx.put("https://dhis2.example/api/trackedEntityTypes/TET1").mock(
        return_value=httpx.Response(200, json={}),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.tracked_entity_types.add_attribute(
            "TET1",
            "TEA_B",
            mandatory=False,
            searchable=True,
        )
    finally:
        await client.close()
    body: dict[str, Any] = _json.loads(put.calls.last.request.read())
    ids = [entry["trackedEntityAttribute"]["id"] for entry in body["trackedEntityTypeAttributes"]]
    assert ids == ["TEA_A", "TEA_B"]
    assert all("trackedEntityType" not in entry for entry in body["trackedEntityTypeAttributes"]), (
        "self-ref must be stripped"
    )
    added = body["trackedEntityTypeAttributes"][1]
    assert added["searchable"] is True
    assert added["mandatory"] is False


@respx.mock
async def test_tet_add_attribute_idempotent_when_already_present() -> None:
    _mock_preamble()
    respx.get("https://dhis2.example/api/trackedEntityTypes/TET1").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "TET1",
                "name": "Person",
                "trackedEntityTypeAttributes": [{"trackedEntityAttribute": {"id": "TEA_A"}}],
            },
        ),
    )
    put = respx.put("https://dhis2.example/api/trackedEntityTypes/TET1").mock(
        return_value=httpx.Response(200, json={}),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.tracked_entity_types.add_attribute("TET1", "TEA_A")
    finally:
        await client.close()
    assert put.called is False


@respx.mock
async def test_tet_remove_attribute_filters_entry() -> None:
    _mock_preamble()
    respx.get("https://dhis2.example/api/trackedEntityTypes/TET1").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "TET1",
                "name": "Person",
                "trackedEntityTypeAttributes": [
                    {"trackedEntityAttribute": {"id": "TEA_A"}},
                    {"trackedEntityAttribute": {"id": "TEA_B"}},
                ],
            },
        ),
    )
    put = respx.put("https://dhis2.example/api/trackedEntityTypes/TET1").mock(
        return_value=httpx.Response(200, json={}),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.tracked_entity_types.remove_attribute("TET1", "TEA_A")
    finally:
        await client.close()
    body: dict[str, Any] = _json.loads(put.calls.last.request.read())
    ids = [entry["trackedEntityAttribute"]["id"] for entry in body["trackedEntityTypeAttributes"]]
    assert ids == ["TEA_B"]


@respx.mock
async def test_tet_delete_routes_to_uid() -> None:
    _mock_preamble()
    route = respx.delete("https://dhis2.example/api/trackedEntityTypes/TET_X").mock(
        return_value=httpx.Response(204),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.tracked_entity_types.delete("TET_X")
    finally:
        await client.close()
    assert route.called


async def test_accessors_bound_on_client() -> None:
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        assert client.tracked_entity_attributes is not None
        assert client.tracked_entity_types is not None
    finally:
        await client.close()
