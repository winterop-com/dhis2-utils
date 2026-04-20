"""Tests for `RoutePayload` + `JsonPatchOp` models in the `route` plugin."""

from __future__ import annotations

import json

import httpx
import pytest
import respx
from dhis2_client import WebMessageResponse
from dhis2_core.plugins.route import service
from dhis2_core.plugins.route.service import JsonPatchOp, RoutePayload
from dhis2_core.profile import Profile


@pytest.fixture(autouse=True)
def _raw_env_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force env-only profile resolution for the tests in this file."""
    monkeypatch.delenv("DHIS2_PROFILE", raising=False)
    monkeypatch.setenv("DHIS2_URL", "http://mock.example")
    monkeypatch.setenv("DHIS2_PAT", "test-token")


def _mock_connect_preamble() -> None:
    """Mock the canonical-URL + `/api/system/info` probes `Dhis2Client.connect()` performs."""
    respx.get("http://mock.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("http://mock.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )


def test_route_payload_round_trips_required_fields() -> None:
    """Minimal payload (code/name/url) round-trips cleanly with extras preserved."""
    payload = RoutePayload.model_validate({"code": "X", "name": "X route", "url": "https://u", "custom": 1})
    assert payload.code == "X"
    assert payload.name == "X route"
    assert payload.url == "https://u"
    dumped = payload.model_dump(exclude_none=True, mode="json")
    assert dumped["custom"] == 1  # preserved via extra="allow"


def test_json_patch_op_from_alias_serialises_to_from() -> None:
    """`from_` attribute alias must serialise to the `from` JSON key for move/copy ops."""
    op = JsonPatchOp.model_validate({"op": "move", "path": "/b", "from": "/a"})
    assert op.from_ == "/a"
    dumped = op.model_dump(by_alias=True, exclude_none=True, mode="json")
    assert dumped == {"op": "move", "path": "/b", "from": "/a"}
    # `populate_by_name=True` lets callers dict-construct via the Python-safe name too.
    op2 = JsonPatchOp.model_validate({"op": "move", "path": "/b", "from_": "/a"})
    assert op2.from_ == "/a"


@respx.mock
async def test_add_route_dumps_payload_to_wire() -> None:
    """`add_route` must serialise the typed payload as the POST body DHIS2 expects."""
    _mock_connect_preamble()
    route = respx.post("http://mock.example/api/routes").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    profile = Profile(base_url="http://mock.example", auth="pat", token="t")
    await service.add_route(
        profile,
        RoutePayload(code="X", name="X route", url="https://u", authorities=["A", "B"]),
    )
    body = json.loads(route.calls.last.request.content)
    assert body == {"code": "X", "name": "X route", "url": "https://u", "authorities": ["A", "B"]}


@respx.mock
async def test_patch_route_sends_list_of_json_patch_ops_on_wire() -> None:
    """Typed `JsonPatchOp` list must serialise to a plain JSON-Patch array body."""
    _mock_connect_preamble()
    route = respx.patch("http://mock.example/api/routes/uid12345678").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    profile = Profile(base_url="http://mock.example", auth="pat", token="t")
    response = await service.patch_route(
        profile,
        "uid12345678",
        [
            JsonPatchOp(op="replace", path="/name", value="renamed"),
            JsonPatchOp.model_validate({"op": "move", "path": "/newPath", "from": "/oldPath"}),
        ],
    )
    assert isinstance(response, WebMessageResponse)
    body = json.loads(route.calls.last.request.content)
    assert body == [
        {"op": "replace", "path": "/name", "value": "renamed"},
        {"op": "move", "path": "/newPath", "from": "/oldPath"},
    ]
