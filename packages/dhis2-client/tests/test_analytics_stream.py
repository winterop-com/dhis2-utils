"""Tests for `Dhis2Client.analytics.stream_to` — streaming analytics exports."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest
import respx
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.errors import AuthenticationError, Dhis2ApiError


def _mock_preamble() -> None:
    """Canonical-URL + /api/system/info probes connect() runs."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )


def _auth() -> BasicAuth:
    """Throwaway auth for test clients."""
    return BasicAuth(username="a", password="b")


@respx.mock
async def test_stream_to_writes_full_body_to_disk(tmp_path: Path) -> None:
    """Single-chunk response streams end-to-end; bytes-on-disk match the canned body."""
    _mock_preamble()
    payload = b'{"headers":[],"rows":[[1],[2],[3]]}'
    respx.get("https://dhis2.example/api/analytics.json").mock(
        return_value=httpx.Response(200, content=payload),
    )

    destination = tmp_path / "out.json"
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        written = await client.analytics.stream_to(
            destination,
            params={"dimension": ["dx:DEancVisit1", "pe:LAST_12_MONTHS"]},
        )
    finally:
        await client.close()

    assert written == len(payload)
    assert destination.read_bytes() == payload


@respx.mock
async def test_stream_to_forwards_repeated_dimension_params(tmp_path: Path) -> None:
    """List-value params land on the wire as repeated query params, as DHIS2 expects."""
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/analytics.json").mock(
        return_value=httpx.Response(200, content=b"{}"),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.analytics.stream_to(
            tmp_path / "out.json",
            params={"dimension": ["dx:X", "pe:Y", "ou:Z"]},
        )
    finally:
        await client.close()

    dimension_values = route.calls.last.request.url.params.get_list("dimension")
    assert dimension_values == ["dx:X", "pe:Y", "ou:Z"]


@respx.mock
async def test_stream_to_accepts_list_of_tuples_params(tmp_path: Path) -> None:
    """`params` also accepts `list[tuple[str, Any]]` — same repeated-param semantics."""
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/analytics.csv").mock(
        return_value=httpx.Response(200, content=b"a,b,c\n1,2,3\n"),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.analytics.stream_to(
            tmp_path / "out.csv",
            params=[("dimension", "dx:X"), ("dimension", "pe:Y")],
            endpoint="/api/analytics.csv",
        )
    finally:
        await client.close()

    assert route.calls.last.request.url.params.get_list("dimension") == ["dx:X", "pe:Y"]


@respx.mock
async def test_stream_to_writes_large_body_without_buffering(tmp_path: Path) -> None:
    """A payload larger than the chunk_size reassembles correctly on disk."""
    _mock_preamble()
    # 10 KB synthetic CSV — larger than chunk_size so aiter_bytes loops.
    payload = b"a,b,c,d\n" + (b"1,2,3,4\n" * 1000)
    respx.get("https://dhis2.example/api/analytics.csv").mock(
        return_value=httpx.Response(200, content=payload),
    )

    destination = tmp_path / "big.csv"
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        written = await client.analytics.stream_to(
            destination,
            params={"dimension": ["dx:X"]},
            endpoint="/api/analytics.csv",
            chunk_size=512,  # force multi-iteration read
        )
    finally:
        await client.close()

    assert written == len(payload)
    assert destination.read_bytes() == payload


@respx.mock
async def test_stream_to_creates_missing_parent_dirs(tmp_path: Path) -> None:
    """Destination's parent directories are created if missing — no pre-mkdir needed."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/analytics.json").mock(
        return_value=httpx.Response(200, content=b"{}"),
    )

    destination = tmp_path / "nested" / "deeper" / "out.json"
    assert not destination.parent.exists()

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.analytics.stream_to(destination, params={"dimension": ["dx:X"]})
    finally:
        await client.close()

    assert destination.parent.is_dir()
    assert destination.read_bytes() == b"{}"


@respx.mock
async def test_stream_to_raises_dhis2_api_error_on_4xx(tmp_path: Path) -> None:
    """Server 4xx short-circuits without writing a partial file."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/analytics.json").mock(
        return_value=httpx.Response(400, json={"httpStatus": "Bad Request", "message": "invalid dimension"}),
    )

    destination = tmp_path / "out.json"
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        with pytest.raises(Dhis2ApiError) as exc_info:
            await client.analytics.stream_to(destination, params={"dimension": ["bad"]})
    finally:
        await client.close()

    assert exc_info.value.status_code == 400
    assert not destination.exists()


@respx.mock
async def test_stream_to_raises_authentication_error_on_401(tmp_path: Path) -> None:
    """401 on the analytics endpoint surfaces as `AuthenticationError`, not `Dhis2ApiError`."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/analytics.json").mock(
        return_value=httpx.Response(401, text="unauthorized"),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        with pytest.raises(AuthenticationError):
            await client.analytics.stream_to(tmp_path / "out.json", params={"dimension": ["dx:X"]})
    finally:
        await client.close()


@respx.mock
async def test_stream_to_supports_non_standard_endpoint(tmp_path: Path) -> None:
    """`/api/analytics/rawData.json` and similar sub-endpoints work via the `endpoint` arg."""
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/analytics/rawData.json").mock(
        return_value=httpx.Response(200, content=b'{"rows":[]}'),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        written = await client.analytics.stream_to(
            tmp_path / "raw.json",
            params={"dimension": ["dx:X"]},
            endpoint="/api/analytics/rawData.json",
        )
    finally:
        await client.close()

    assert route.call_count == 1
    assert written == 11  # len(b'{"rows":[]}')


async def test_stream_to_rejects_unconnected_client(tmp_path: Path) -> None:
    """Calling before `connect()` raises a clear RuntimeError."""
    client = Dhis2Client("https://dhis2.example", auth=_auth())
    with pytest.raises(RuntimeError, match="not connected"):
        await client.analytics.stream_to(tmp_path / "out.json", params={"dimension": ["dx:X"]})
