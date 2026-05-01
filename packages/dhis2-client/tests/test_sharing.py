"""Unit tests for the typed sharing helpers."""

from __future__ import annotations

import httpx
import pytest
import respx
from dhis2_client import (
    ACCESS_NONE,
    ACCESS_READ_METADATA,
    ACCESS_READ_WRITE_DATA,
    ACCESS_READ_WRITE_METADATA,
    BasicAuth,
    Dhis2Client,
    SharingBuilder,
    access_string,
    apply_sharing,
    get_sharing,
)


def test_access_string_composes_eight_chars() -> None:
    assert access_string() == "--------"
    assert access_string(metadata="rw") == "rw------"
    assert access_string(metadata="r-", data="r-") == "r-r-----"
    assert access_string(metadata="rw", data="rw") == "rwrw----"


def test_access_constants_match_expected_wire_strings() -> None:
    """The constants line up with access_string() for the common forms."""
    assert access_string() == ACCESS_NONE
    assert access_string(metadata="r-") == ACCESS_READ_METADATA
    assert access_string(metadata="rw") == ACCESS_READ_WRITE_METADATA
    assert access_string(metadata="rw", data="rw") == ACCESS_READ_WRITE_DATA


def test_builder_accumulates_grants_without_mutation() -> None:
    """grant_user / grant_user_group return new builders; original is untouched."""
    one = SharingBuilder(public_access=ACCESS_READ_METADATA, owner_user_id="adminUID_12")
    two = one.grant_user("userUID_0001", ACCESS_READ_WRITE_DATA)
    three = two.grant_user_group("groupUID_001", ACCESS_READ_METADATA)
    assert one.user_accesses == {}
    assert two.user_accesses == {"userUID_0001": ACCESS_READ_WRITE_DATA}
    assert three.user_group_accesses == {"groupUID_001": ACCESS_READ_METADATA}

    wire = three.to_sharing_object()
    assert wire.publicAccess == ACCESS_READ_METADATA
    assert wire.user is not None and wire.user.id == "adminUID_12"
    assert wire.userAccesses is not None
    assert len(wire.userAccesses) == 1 and wire.userAccesses[0].id == "userUID_0001"
    assert wire.userGroupAccesses is not None
    assert len(wire.userGroupAccesses) == 1 and wire.userGroupAccesses[0].id == "groupUID_001"


def _stub_connect_routes() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))


@pytest.fixture
async def client() -> Dhis2Client:
    return Dhis2Client("https://dhis2.example", auth=BasicAuth(username="admin", password="district"))


@respx.mock
async def test_get_sharing_unwraps_info_envelope(client: Dhis2Client) -> None:
    """`SharingInfo` wraps the object; `get_sharing` strips the wrapper for callers."""
    _stub_connect_routes()
    respx.get("https://dhis2.example/api/sharing", params={"type": "dataSet", "id": "dsUID123"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "meta": {"allowPublicAccess": True},
                "object": {
                    "id": "dsUID123",
                    "name": "Test",
                    "publicAccess": "r-------",
                    "externalAccess": False,
                    "user": {"id": "adminUID", "name": "admin"},
                    "userAccesses": [],
                    "userGroupAccesses": [],
                },
            },
        ),
    )
    async with client as c:
        sharing = await get_sharing(c, "dataSet", "dsUID123")
    assert sharing.id == "dsUID123"
    assert sharing.publicAccess == "r-------"


@respx.mock
async def test_apply_sharing_posts_object_wrapper(client: Dhis2Client) -> None:
    """The wire format of POST /api/sharing wraps the SharingObject under `object`."""
    _stub_connect_routes()
    route = respx.post(
        "https://dhis2.example/api/sharing",
        params={"type": "dataSet", "id": "dsUID123"},
    ).mock(return_value=httpx.Response(200, json={"httpStatus": "OK", "status": "OK"}))
    builder = (
        SharingBuilder(public_access=ACCESS_READ_METADATA, owner_user_id="adminUID_12")
        .grant_user("userUID_0001", ACCESS_READ_WRITE_DATA)
        .grant_user_group("groupUID_001", ACCESS_READ_METADATA)
    )
    async with client as c:
        envelope = await apply_sharing(c, "dataSet", "dsUID123", builder)
    assert envelope.status == "OK"
    assert route.called
    import json as _json

    body = _json.loads(route.calls.last.request.content)
    assert "object" in body
    obj = body["object"]
    assert obj["publicAccess"] == ACCESS_READ_METADATA
    assert obj["user"]["id"] == "adminUID_12"
    assert obj["userAccesses"] == [{"id": "userUID_0001", "access": ACCESS_READ_WRITE_DATA}]
    assert obj["userGroupAccesses"] == [{"id": "groupUID_001", "access": ACCESS_READ_METADATA}]


@respx.mock
async def test_apply_sharing_accepts_raw_sharing_object(client: Dhis2Client) -> None:
    """Callers can pass a raw SharingObject instead of the builder."""
    _stub_connect_routes()
    from dhis2_client.generated.v42.oas import SharingObject

    route = respx.post(
        "https://dhis2.example/api/sharing",
        params={"type": "dataElement", "id": "deUID123456"},
    ).mock(return_value=httpx.Response(200, json={"status": "OK"}))
    sharing = SharingObject(publicAccess=ACCESS_READ_METADATA, externalAccess=False)
    async with client as c:
        await apply_sharing(c, "dataElement", "deUID123456", sharing)
    assert route.called
