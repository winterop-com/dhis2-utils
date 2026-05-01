"""Unit tests for `MetadataAccessor.apply_sharing_bulk` + `.apply_sharing_bulk_multi` — respx-mocked."""

from __future__ import annotations

import json as _json

import httpx
import respx
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.metadata import BulkSharingResult
from dhis2_client.sharing import ACCESS_READ_METADATA, ACCESS_READ_WRITE_METADATA, SharingBuilder


def _auth() -> BasicAuth:
    return BasicAuth(username="admin", password="district")


def _mock_preamble() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.0"}),
    )


@respx.mock
async def test_apply_sharing_bulk_fans_out_per_uid_and_reports_successes() -> None:
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/sharing").mock(return_value=httpx.Response(200, json={}))
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        builder = SharingBuilder(public_access=ACCESS_READ_METADATA).grant_user_group("UG_PROG", "rwrw----")
        result = await client.metadata.apply_sharing_bulk("dataSet", ["DS_A", "DS_B"], builder)
    finally:
        await client.close()
    assert route.call_count == 2
    assert isinstance(result, BulkSharingResult)
    assert result.ok is True
    assert sorted(result.successful_uids) == ["DS_A", "DS_B"]
    assert result.total == 2


@respx.mock
async def test_apply_sharing_bulk_sends_per_uid_query_params_and_object_payload() -> None:
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/sharing").mock(return_value=httpx.Response(200, json={}))
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        builder = SharingBuilder(public_access=ACCESS_READ_WRITE_METADATA).grant_user("U_ALICE", "rw------")
        await client.metadata.apply_sharing_bulk("dataSet", ["DS_A"], builder)
    finally:
        await client.close()
    request = route.calls.last.request
    assert request.url.params["type"] == "dataSet"
    assert request.url.params["id"] == "DS_A"
    body = _json.loads(request.read())
    assert body["object"]["publicAccess"] == ACCESS_READ_WRITE_METADATA
    assert body["object"]["userAccesses"] == [{"id": "U_ALICE", "access": "rw------"}]


@respx.mock
async def test_apply_sharing_bulk_captures_per_uid_failures_without_raising() -> None:
    _mock_preamble()
    respx.post("https://dhis2.example/api/sharing", params={"type": "dataSet", "id": "DS_A"}).mock(
        return_value=httpx.Response(200, json={}),
    )
    respx.post("https://dhis2.example/api/sharing", params={"type": "dataSet", "id": "DS_B"}).mock(
        return_value=httpx.Response(
            409,
            json={"status": "ERROR", "message": "conflict on sharing", "httpStatusCode": 409},
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        builder = SharingBuilder(public_access=ACCESS_READ_METADATA)
        result = await client.metadata.apply_sharing_bulk("dataSet", ["DS_A", "DS_B"], builder)
    finally:
        await client.close()
    assert result.ok is False
    assert result.successful_uids == ["DS_A"]
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.uid == "DS_B"
    assert failure.resource == "dataSet"
    assert failure.status_code == 409
    assert "conflict" in failure.message.lower()


@respx.mock
async def test_apply_sharing_bulk_multi_fans_out_across_resource_types() -> None:
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/sharing").mock(return_value=httpx.Response(200, json={}))
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.apply_sharing_bulk_multi(
            {
                "dataSet": ["DS_A"],
                "program": ["PROG_A"],
            },
            SharingBuilder(public_access=ACCESS_READ_METADATA),
        )
    finally:
        await client.close()
    assert route.call_count == 2
    assert sorted(result.successful_uids) == ["DS_A", "PROG_A"]
    assert result.ok is True


@respx.mock
async def test_apply_sharing_bulk_short_circuits_on_empty_input() -> None:
    _mock_preamble()
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.apply_sharing_bulk(
            "dataSet", [], SharingBuilder(public_access=ACCESS_READ_METADATA)
        )
    finally:
        await client.close()
    assert result.ok is True
    assert result.total == 0
    assert result.successful_uids == []
