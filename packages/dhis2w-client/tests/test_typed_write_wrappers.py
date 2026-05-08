"""Tests for `Dhis2Client.post` / `put` typed-response wrappers."""

from __future__ import annotations

import httpx
import respx
from dhis2w_client import BasicAuth, Dhis2Client, WebMessageResponse


def _auth() -> BasicAuth:
    return BasicAuth(username="a", password="b")


def _mock_preamble() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.0"}),
    )


@respx.mock
async def test_post_parses_into_web_message_response() -> None:
    _mock_preamble()
    respx.post("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(
            201,
            json={
                "status": "OK",
                "httpStatus": "Created",
                "httpStatusCode": 201,
                "message": "done",
                "response": {"uid": "DE_NEW00001"},
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        envelope = await client.post(
            "/api/dataElements",
            {"name": "x"},
            model=WebMessageResponse,
        )
    finally:
        await client.close()
    assert isinstance(envelope, WebMessageResponse)
    assert envelope.status is not None
    assert envelope.status.value == "OK"
    assert envelope.created_uid == "DE_NEW00001"


@respx.mock
async def test_put_parses_into_web_message_response_with_params() -> None:
    _mock_preamble()
    route = respx.put("https://dhis2.example/api/programs/PRG1").mock(
        return_value=httpx.Response(
            200,
            json={
                "status": "OK",
                "httpStatus": "OK",
                "httpStatusCode": 200,
                "message": "updated",
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        envelope = await client.put(
            "/api/programs/PRG1",
            {"id": "PRG1", "name": "x"},
            model=WebMessageResponse,
            params={"mergeMode": "REPLACE"},
        )
    finally:
        await client.close()
    assert isinstance(envelope, WebMessageResponse)
    assert route.calls.last.request.url.params["mergeMode"] == "REPLACE"
