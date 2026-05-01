"""Unit tests for the hand-written SystemModule (system/info, me)."""

from __future__ import annotations

import httpx
import respx
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.system import DhisCalendar


@respx.mock
async def test_system_info_parses_model() -> None:
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(
            200,
            json={"version": "2.44-SNAPSHOT", "revision": "abc1234", "systemName": "DHIS2 Play"},
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        info = await client.system.info()
    finally:
        await client.close()
    assert info.version == "2.44-SNAPSHOT"
    assert info.revision == "abc1234"
    assert info.systemName == "DHIS2 Play"


@respx.mock
async def test_me_parses_model() -> None:
    respx.get("https://dhis2.example/api/me").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "xY123",
                "username": "system",
                "displayName": "System User",
                "authorities": ["ALL"],
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        me = await client.system.me()
    finally:
        await client.close()
    assert me.id == "xY123"
    assert me.username == "system"
    assert me.authorities == ["ALL"]


@respx.mock
async def test_me_coerces_bare_uid_strings_to_display_refs() -> None:
    """`/api/me` returns `programs` as bare UID strings in v42; `Me` lifts them to `DisplayRef(id=...)`.

    Regression guard for the `Me` typing introduced in #71 — a direct
    `client.system.me()` call used to blow up pydantic validation because the
    server shape didn't match the typed `list[DisplayRef]` annotation. The
    validator on every ref-list field coerces strings to `{id: string}` refs.
    """
    respx.get("https://dhis2.example/api/me").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "xY123",
                "username": "admin",
                "programs": ["kNYyyzd0DLp", "eke95YJi9VS"],  # bare-UID case DHIS2 actually returns
                "userGroups": [{"id": "fKCkReZEyUN", "displayName": "Administrators"}],  # typed case still works
                "organisationUnits": ["NORNordland"],  # mixed across fields
            },
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        me = await client.system.me()
    finally:
        await client.close()
    assert me.programs is not None
    assert [p.id for p in me.programs] == ["kNYyyzd0DLp", "eke95YJi9VS"]
    assert all(p.displayName is None for p in me.programs)  # no displayName in bare-UID case
    assert me.userGroups is not None
    assert me.userGroups[0].id == "fKCkReZEyUN"
    assert me.userGroups[0].displayName == "Administrators"
    assert me.organisationUnits is not None
    assert me.organisationUnits[0].id == "NORNordland"


@respx.mock
async def test_calendar_returns_value_from_setting() -> None:
    """`SystemModule.calendar()` reads `keyCalendar` and returns its value."""
    respx.get("https://dhis2.example/api/systemSettings/keyCalendar").mock(
        return_value=httpx.Response(200, json={"keyCalendar": "ethiopian"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        value = await client.system.calendar()
    finally:
        await client.close()
    assert value == "ethiopian"


@respx.mock
async def test_calendar_falls_back_to_iso8601_when_unset() -> None:
    """When `keyCalendar` is unset (4xx or empty), `calendar()` returns the server default `iso8601`."""
    respx.get("https://dhis2.example/api/systemSettings/keyCalendar").mock(
        return_value=httpx.Response(404, json={}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        value = await client.system.calendar()
    finally:
        await client.close()
    assert value == DhisCalendar.ISO8601.value


@respx.mock
async def test_set_calendar_posts_text_plain_body() -> None:
    """`SystemModule.set_calendar()` POSTs `text/plain` to `/api/systemSettings/keyCalendar`."""
    route = respx.post("https://dhis2.example/api/systemSettings/keyCalendar").mock(
        return_value=httpx.Response(200, json={"httpStatus": "OK", "status": "OK"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    try:
        await client.system.set_calendar(DhisCalendar.NEPALI)
    finally:
        await client.close()
    assert route.called
    request = route.calls[0].request
    assert request.headers["content-type"].startswith("text/plain")
    assert request.content == b"nepali"
