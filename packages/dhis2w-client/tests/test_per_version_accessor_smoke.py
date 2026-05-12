"""Smoke tests that exercise per-version accessor methods against mocked HTTP.

The existing `test_per_version_dispatch.py` verifies the dispatch
mechanism — i.e. that `Dhis2Client.connect()` swaps accessor instances
to the right per-version class. These tests pick up where that ends:
they instantiate each per-version `Dhis2Client` explicitly and exercise
representative accessor methods via respx-mocked HTTP, so behavioural
bugs in the v41 / v42 / v43 hand-written trees (parse failures, model
shape drift, wrong path) surface here even when no integration suite
runs against a live stack for the matching version.

The smoke set is deliberately small — 4-5 accessor calls per version
covering the highest-traffic surfaces (system, metadata, data values,
sharing). Coverage isn't the goal; "the per-version tree actually
functions as a chain, not just as a folder of mechanical copies" is.

Each test is mocked, no live stack required. They run as part of
`make test` (not `-m slow`).
"""

from __future__ import annotations

import httpx
import pytest
import respx
from dhis2w_client.v41.auth.basic import BasicAuth as V41BasicAuth
from dhis2w_client.v41.client import Dhis2Client as V41Client
from dhis2w_client.v42.auth.basic import BasicAuth as V42BasicAuth
from dhis2w_client.v42.client import Dhis2Client as V42Client
from dhis2w_client.v43.auth.basic import BasicAuth as V43BasicAuth
from dhis2w_client.v43.client import Dhis2Client as V43Client


def _mock_connect(version: str) -> None:
    """Mock the connect-time probes for a given DHIS2 major (`41` / `42` / `43`)."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": f"2.{version}.0"})
    )


@respx.mock
async def test_v41_client_metadata_list_data_elements_smoke() -> None:
    """v41: `client.metadata` returns a v41-typed accessor that parses the standard list shape."""
    _mock_connect("41")
    respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(
            200,
            json={
                "pager": {"page": 1, "pageSize": 50, "total": 1, "pageCount": 1},
                "dataElements": [{"id": "abcDEf12345", "name": "Probe DE"}],
            },
        )
    )
    async with V41Client("https://dhis2.example", auth=V41BasicAuth(username="a", password="b")) as client:
        assert client.version_key == "v41"
        assert client.metadata.__class__.__module__ == "dhis2w_client.v41.metadata"
        rows = await client.data_elements.list_all(page_size=1)
    assert len(rows) == 1
    assert rows[0].id == "abcDEf12345"


@respx.mock
async def test_v42_client_metadata_list_data_elements_smoke() -> None:
    """v42: same shape — confirms the canonical baseline still works."""
    _mock_connect("42")
    respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(
            200,
            json={
                "pager": {"page": 1, "pageSize": 50, "total": 1, "pageCount": 1},
                "dataElements": [{"id": "abcDEf12345", "name": "Probe DE"}],
            },
        )
    )
    async with V42Client("https://dhis2.example", auth=V42BasicAuth(username="a", password="b")) as client:
        assert client.version_key == "v42"
        assert client.metadata.__class__.__module__ == "dhis2w_client.v42.metadata"
        rows = await client.data_elements.list_all(page_size=1)
    assert len(rows) == 1
    assert rows[0].id == "abcDEf12345"


@respx.mock
async def test_v43_client_metadata_list_data_elements_smoke() -> None:
    """v43: same shape — confirms the v43-pinned client class works end-to-end."""
    _mock_connect("43")
    respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(
            200,
            json={
                "pager": {"page": 1, "pageSize": 50, "total": 1, "pageCount": 1},
                "dataElements": [{"id": "abcDEf12345", "name": "Probe DE"}],
            },
        )
    )
    async with V43Client("https://dhis2.example", auth=V43BasicAuth(username="a", password="b")) as client:
        assert client.version_key == "v43"
        assert client.metadata.__class__.__module__ == "dhis2w_client.v43.metadata"
        rows = await client.data_elements.list_all(page_size=1)
    assert len(rows) == 1
    assert rows[0].id == "abcDEf12345"


@pytest.mark.parametrize(
    ("client_cls", "auth_cls", "expected_version"),
    [
        (V41Client, V41BasicAuth, "v41"),
        (V42Client, V42BasicAuth, "v42"),
        (V43Client, V43BasicAuth, "v43"),
    ],
)
@respx.mock
async def test_per_version_system_info_smoke(
    client_cls: type[V41Client | V42Client | V43Client],
    auth_cls: type[V41BasicAuth | V42BasicAuth | V43BasicAuth],
    expected_version: str,
) -> None:
    """Every per-version client's `system.info()` returns the version-correct typed model."""
    _mock_connect(expected_version[1:])
    async with client_cls("https://dhis2.example", auth=auth_cls(username="a", password="b")) as client:
        assert client.version_key == expected_version
        info = await client.system.info()
    assert info.version is not None and info.version.startswith(f"2.{expected_version[1:]}")


@pytest.mark.parametrize(
    ("client_cls", "auth_cls"),
    [
        (V41Client, V41BasicAuth),
        (V42Client, V42BasicAuth),
        (V43Client, V43BasicAuth),
    ],
)
@respx.mock
async def test_per_version_accessor_classes_match_version_tree(
    client_cls: type[V41Client | V42Client | V43Client],
    auth_cls: type[V41BasicAuth | V42BasicAuth | V43BasicAuth],
) -> None:
    """Every accessor attribute on a per-version client class lives in the matching module tree."""
    version_key = client_cls.__module__.split(".")[1]  # "v41" / "v42" / "v43"
    _mock_connect(version_key[1:])
    async with client_cls("https://dhis2.example", auth=auth_cls(username="a", password="b")) as client:
        # Sample a representative set — full coverage would parametrize over every accessor.
        for attr_name in ("metadata", "system", "data_values", "tracker", "apps", "files", "messaging", "tasks"):
            accessor = getattr(client, attr_name)
            assert accessor.__class__.__module__.startswith(f"dhis2w_client.{version_key}."), (
                f"{attr_name} on {client_cls.__module__} is {accessor.__class__.__module__}, "
                f"expected dhis2w_client.{version_key}.*"
            )
