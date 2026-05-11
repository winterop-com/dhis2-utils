"""Unit tests for `MetadataAccessor.patch_bulk` + `.patch_bulk_multi` — respx-mocked."""

from __future__ import annotations

import json as _json
from typing import Any

import httpx
import respx
from dhis2w_client import BasicAuth, BulkPatchResult, Dhis2Client, ReplaceOp


def _auth() -> BasicAuth:
    return BasicAuth(username="admin", password="district")


def _mock_preamble() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.0"}),
    )


@respx.mock
async def test_patch_bulk_fans_out_per_uid_and_reports_successes() -> None:
    """Patch bulk fans out per uid and reports successes."""
    _mock_preamble()
    a = respx.patch("https://dhis2.example/api/dataElements/DE_A").mock(return_value=httpx.Response(200, json={}))
    b = respx.patch("https://dhis2.example/api/dataElements/DE_B").mock(return_value=httpx.Response(200, json={}))
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.patch_bulk(
            "dataElements",
            [
                ("DE_A", [ReplaceOp(op="replace", path="/name", value="Renamed A")]),
                ("DE_B", [ReplaceOp(op="replace", path="/name", value="Renamed B")]),
            ],
        )
    finally:
        await client.close()
    assert a.called and b.called
    assert isinstance(result, BulkPatchResult)
    assert result.ok is True
    assert sorted(result.successful_uids) == ["DE_A", "DE_B"]
    assert result.failures == []


@respx.mock
async def test_patch_bulk_sends_json_patch_body_with_typed_ops() -> None:
    """Patch bulk sends json patch body with typed ops."""
    _mock_preamble()
    route = respx.patch("https://dhis2.example/api/dataElements/DE_A").mock(return_value=httpx.Response(200, json={}))
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.metadata.patch_bulk(
            "dataElements",
            [("DE_A", [ReplaceOp(op="replace", path="/shortName", value="A2")])],
        )
    finally:
        await client.close()
    body: list[dict[str, Any]] = _json.loads(route.calls.last.request.read())
    assert body == [{"op": "replace", "path": "/shortName", "value": "A2"}]
    assert route.calls.last.request.headers["Content-Type"] == "application/json-patch+json"


@respx.mock
async def test_patch_bulk_captures_per_uid_failures_without_raising() -> None:
    """Patch bulk captures per uid failures without raising."""
    _mock_preamble()
    respx.patch("https://dhis2.example/api/dataElements/DE_A").mock(return_value=httpx.Response(200, json={}))
    respx.patch("https://dhis2.example/api/dataElements/DE_B").mock(
        return_value=httpx.Response(
            409,
            json={"status": "ERROR", "message": "conflict on /name", "httpStatusCode": 409},
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.patch_bulk(
            "dataElements",
            [
                ("DE_A", [{"op": "replace", "path": "/name", "value": "ok"}]),
                ("DE_B", [{"op": "replace", "path": "/name", "value": "bad"}]),
            ],
        )
    finally:
        await client.close()
    assert result.ok is False
    assert result.successful_uids == ["DE_A"]
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.uid == "DE_B"
    assert failure.resource == "dataElements"
    assert failure.status_code == 409
    assert "conflict" in failure.message.lower()


@respx.mock
async def test_patch_bulk_multi_fans_out_across_resource_types() -> None:
    """Patch bulk multi fans out across resource types."""
    _mock_preamble()
    de = respx.patch("https://dhis2.example/api/dataElements/DE_A").mock(return_value=httpx.Response(200, json={}))
    ind = respx.patch("https://dhis2.example/api/indicators/IND_A").mock(return_value=httpx.Response(200, json={}))
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.patch_bulk_multi(
            {
                "dataElements": [("DE_A", [{"op": "replace", "path": "/name", "value": "de"}])],
                "indicators": [("IND_A", [{"op": "replace", "path": "/name", "value": "ind"}])],
            },
        )
    finally:
        await client.close()
    assert de.called and ind.called
    assert sorted(result.successful_uids) == ["DE_A", "IND_A"]


@respx.mock
async def test_patch_bulk_short_circuits_on_empty_input() -> None:
    """Patch bulk short circuits on empty input."""
    _mock_preamble()
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.patch_bulk("dataElements", [])
    finally:
        await client.close()
    assert result.ok is True
    assert result.total == 0
    assert result.failures == []


async def test_bulk_patch_result_helpers() -> None:
    """Bulk patch result helpers."""
    empty = BulkPatchResult()
    assert empty.ok is True
    assert empty.total == 0

    mixed = BulkPatchResult(
        successful_uids=["A", "B"],
        failures=[],
    )
    assert mixed.ok is True
    assert mixed.total == 2
