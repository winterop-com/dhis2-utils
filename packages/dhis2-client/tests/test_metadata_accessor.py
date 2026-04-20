"""Tests for `Dhis2Client.metadata.delete_bulk` + `delete_bulk_multi`."""

from __future__ import annotations

import json

import httpx
import respx
from dhis2_client import BasicAuth, Dhis2Client


def _mock_preamble() -> None:
    """Stub the canonical-URL + /api/system/info probes `connect()` performs."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )


def _auth() -> BasicAuth:
    """Throwaway auth for test clients."""
    return BasicAuth(username="a", password="b")


@respx.mock
async def test_delete_bulk_posts_minimal_bundle_and_returns_webmessage() -> None:
    """`delete_bulk` POSTs `{resource: [{id: ...}]}` with the DELETE importStrategy."""
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/metadata").mock(
        return_value=httpx.Response(
            200,
            json={
                "httpStatus": "OK",
                "httpStatusCode": 200,
                "status": "OK",
                "message": "",
                "response": {
                    "status": "OK",
                    "stats": {"deleted": 2, "created": 0, "updated": 0, "ignored": 0, "total": 2},
                    "typeReports": [
                        {
                            "klass": "org.hisp.dhis.dataelement.DataElement",
                            "stats": {"deleted": 2, "total": 2},
                        }
                    ],
                },
            },
        ),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.delete_bulk("dataElements", ["deUidAAA0001", "deUidBBB0002"])
    finally:
        await client.close()

    assert route.call_count == 1
    call = route.calls.last
    params = call.request.url.params
    assert params["importStrategy"] == "DELETE"
    assert params["atomicMode"] == "NONE"
    body = json.loads(call.request.content)
    assert body == {"dataElements": [{"id": "deUidAAA0001"}, {"id": "deUidBBB0002"}]}

    report = result.import_report()
    assert report is not None
    assert report.stats is not None
    assert report.stats.deleted == 2


@respx.mock
async def test_delete_bulk_empty_uids_short_circuits_without_http() -> None:
    """An empty UID list returns a no-op WebMessage without making an HTTP call."""
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/metadata")

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.delete_bulk("dataElements", [])
    finally:
        await client.close()

    assert route.call_count == 0
    assert result.status == "OK"
    assert result.message == "no uids supplied"


@respx.mock
async def test_delete_bulk_multi_merges_multiple_resource_types() -> None:
    """`delete_bulk_multi` builds one bundle spanning every supplied resource type."""
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/metadata").mock(
        return_value=httpx.Response(
            200,
            json={
                "httpStatus": "OK",
                "httpStatusCode": 200,
                "status": "OK",
                "response": {"status": "OK", "stats": {"deleted": 3, "total": 3}, "typeReports": []},
            },
        ),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.metadata.delete_bulk_multi(
            {
                "dataElements": ["deUidAAA0001"],
                "indicators": ["indUidAAA001", "indUidBBB002"],
            }
        )
    finally:
        await client.close()

    body = json.loads(route.calls.last.request.content)
    assert body == {
        "dataElements": [{"id": "deUidAAA0001"}],
        "indicators": [{"id": "indUidAAA001"}, {"id": "indUidBBB002"}],
    }


@respx.mock
async def test_delete_bulk_multi_skips_empty_resource_entries() -> None:
    """Resource keys whose UID list is empty are dropped from the wire bundle."""
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/metadata").mock(
        return_value=httpx.Response(200, json={"status": "OK", "httpStatus": "OK", "httpStatusCode": 200}),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.metadata.delete_bulk_multi(
            {
                "dataElements": ["deUidAAA0001"],
                "indicators": [],  # skipped
            }
        )
    finally:
        await client.close()

    body = json.loads(route.calls.last.request.content)
    assert "dataElements" in body
    assert "indicators" not in body


@respx.mock
async def test_delete_bulk_multi_all_empty_short_circuits() -> None:
    """Every-list-empty payload never hits the wire."""
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/metadata")

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        result = await client.metadata.delete_bulk_multi({"dataElements": [], "indicators": []})
    finally:
        await client.close()

    assert route.call_count == 0
    assert result.status == "OK"


@respx.mock
async def test_delete_bulk_forwards_atomic_mode_parameter() -> None:
    """`atomic_mode='ALL'` flows through as a query parameter."""
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/metadata").mock(
        return_value=httpx.Response(200, json={"status": "OK", "httpStatus": "OK", "httpStatusCode": 200}),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.metadata.delete_bulk_multi(
            {"dataElements": ["deUidAAA0001"]},
            atomic_mode="ALL",
        )
    finally:
        await client.close()

    assert route.calls.last.request.url.params["atomicMode"] == "ALL"
