"""Tests for `RoutePayload` + `JsonPatchOp` discriminated Union in the `route` plugin."""

from __future__ import annotations

import json

import httpx
import pytest
import respx
from dhis2_client import (
    AddOp,
    CopyOp,
    JsonPatchOpAdapter,
    MoveOp,
    RemoveOp,
    ReplaceOp,
    TestOp,
    WebMessageResponse,
)
from dhis2_core.plugins.route import service
from dhis2_core.plugins.route.service import RoutePayload
from dhis2_core.profile import Profile
from pydantic import ValidationError


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


def test_json_patch_op_discriminator_picks_add() -> None:
    """`{op: add}` routes through the discriminator to `AddOp`; `value` is required."""
    op = JsonPatchOpAdapter.validate_python({"op": "add", "path": "/name", "value": "foo"})
    assert isinstance(op, AddOp)
    assert op.value == "foo"


def test_json_patch_op_discriminator_picks_remove() -> None:
    """`{op: remove}` routes to `RemoveOp`; no `value` / `from` allowed (extra='forbid')."""
    op = JsonPatchOpAdapter.validate_python({"op": "remove", "path": "/legacy"})
    assert isinstance(op, RemoveOp)


def test_json_patch_op_discriminator_picks_move_with_from_alias() -> None:
    """`{op: move}` routes to `MoveOp`; JSON `from` key maps to the Python `from_` alias."""
    op = JsonPatchOpAdapter.validate_python({"op": "move", "path": "/b", "from": "/a"})
    assert isinstance(op, MoveOp)
    assert op.from_ == "/a"
    dumped = op.model_dump(by_alias=True, exclude_none=True, mode="json")
    assert dumped == {"op": "move", "path": "/b", "from": "/a"}


def test_json_patch_op_move_rejects_missing_from() -> None:
    """`MoveOp` requires `from_`; the adapter rejects payloads without it."""
    with pytest.raises(ValidationError) as exc_info:
        JsonPatchOpAdapter.validate_python({"op": "move", "path": "/b"})
    assert "from" in str(exc_info.value).lower()


def test_json_patch_op_remove_rejects_extra_value_field() -> None:
    """`RemoveOp` has `extra='forbid'`; callers passing a `value` get a validation error instead of a silent success."""
    with pytest.raises(ValidationError):
        JsonPatchOpAdapter.validate_python({"op": "remove", "path": "/x", "value": "should-not-apply"})


def test_json_patch_op_copy_picks_copyop_variant() -> None:
    """`{op: copy}` routes to `CopyOp`."""
    op = JsonPatchOpAdapter.validate_python({"op": "copy", "path": "/b", "from": "/a"})
    assert isinstance(op, CopyOp)
    assert op.from_ == "/a"


def test_json_patch_op_test_requires_value() -> None:
    """`{op: test}` routes to `TestOp` and requires `value`."""
    op = JsonPatchOpAdapter.validate_python({"op": "test", "path": "/x", "value": 42})
    assert isinstance(op, TestOp)
    assert op.value == 42


def test_json_patch_op_rejects_unknown_op() -> None:
    """Unknown `op` tags fail the discriminator lookup cleanly."""
    with pytest.raises(ValidationError):
        JsonPatchOpAdapter.validate_python({"op": "nonsense", "path": "/x"})


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
async def test_patch_route_sends_typed_ops_as_plain_json_patch_array() -> None:
    """Typed op variants serialise to the RFC 6902 wire shape, `from_` alias → `from` key."""
    _mock_connect_preamble()
    route = respx.patch("http://mock.example/api/routes/uid12345678").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    profile = Profile(base_url="http://mock.example", auth="pat", token="t")
    response = await service.patch_route(
        profile,
        "uid12345678",
        [
            ReplaceOp(path="/name", value="renamed"),
            JsonPatchOpAdapter.validate_python({"op": "move", "path": "/newPath", "from": "/oldPath"}),
            RemoveOp(path="/stale"),
        ],
    )
    assert isinstance(response, WebMessageResponse)
    body = json.loads(route.calls.last.request.content)
    assert body == [
        {"op": "replace", "path": "/name", "value": "renamed"},
        {"op": "move", "path": "/newPath", "from": "/oldPath"},
        {"op": "remove", "path": "/stale"},
    ]
