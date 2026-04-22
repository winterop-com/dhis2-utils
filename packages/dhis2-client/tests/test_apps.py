"""Tests for `Dhis2Client.apps` — /api/apps + /api/appHub wiring."""

from __future__ import annotations

from pathlib import Path

import httpx
import respx
from dhis2_client import BasicAuth, Dhis2Client


def _mock_preamble() -> None:
    """Canonical-URL + /api/system/info probes connect() runs."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )


def _auth() -> BasicAuth:
    """Throwaway auth for test clients."""
    return BasicAuth(username="a", password="b")


_INSTALLED_APPS_PAYLOAD = [
    {
        "key": "dashboard-widget",
        "name": "Dashboard Widget",
        "displayName": "Dashboard Widget",
        "version": "1.0.0",
        "appType": "DASHBOARD_WIDGET",
        "bundled": False,
        "app_hub_id": "hub-widget-001",
    },
    {
        "key": "core-import-export",
        "name": "Import/Export",
        "version": "42.0.0",
        "bundled": True,
    },
]

_HUB_PAYLOAD = [
    {
        "id": "hub-widget-001",
        "name": "Dashboard Widget",
        "versions": [
            {"id": "ver-100", "version": "1.0.0"},
            {"id": "ver-200", "version": "2.0.0"},
        ],
    },
]


@respx.mock
async def test_list_apps_parses_installed_rows() -> None:
    """GET /api/apps → typed list[App]; bundled + non-bundled both land."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/apps").mock(
        return_value=httpx.Response(200, json=_INSTALLED_APPS_PAYLOAD),
    )
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        apps = await client.apps.list_apps()
    assert len(apps) == 2
    widget = next(a for a in apps if a.key == "dashboard-widget")
    assert widget.version == "1.0.0"
    assert widget.app_hub_id == "hub-widget-001"
    assert widget.bundled is False
    core = next(a for a in apps if a.key == "core-import-export")
    assert core.bundled is True


@respx.mock
async def test_get_returns_none_when_key_not_installed() -> None:
    """`apps.get('missing')` falls through to None rather than raising."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/apps").mock(return_value=httpx.Response(200, json=_INSTALLED_APPS_PAYLOAD))
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        assert await client.apps.get("missing") is None
        hit = await client.apps.get("dashboard-widget")
        assert hit is not None
        assert hit.version == "1.0.0"


@respx.mock
async def test_install_from_file_posts_multipart(tmp_path: Path) -> None:
    """`install_from_file` uploads the zip as `file=` in multipart/form-data."""
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/apps").mock(return_value=httpx.Response(204))
    zip_path = tmp_path / "widget.zip"
    zip_path.write_bytes(b"fake-zip-bytes")
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        await client.apps.install_from_file(zip_path)
    assert route.called
    body = route.calls.last.request.content
    # multipart bodies contain the filename + content-type headers; spot-check them.
    assert b'filename="widget.zip"' in body
    assert b"application/zip" in body
    assert b"fake-zip-bytes" in body


@respx.mock
async def test_install_from_hub_posts_to_versioned_path() -> None:
    """`install_from_hub('abc')` → POST /api/appHub/abc."""
    _mock_preamble()
    route = respx.post("https://dhis2.example/api/appHub/abc-123").mock(return_value=httpx.Response(201))
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        await client.apps.install_from_hub("abc-123")
    assert route.called


@respx.mock
async def test_uninstall_calls_delete_on_app_key() -> None:
    """`uninstall('k')` → DELETE /api/apps/k."""
    _mock_preamble()
    route = respx.delete("https://dhis2.example/api/apps/my-app").mock(return_value=httpx.Response(204))
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        await client.apps.uninstall("my-app")
    assert route.called


@respx.mock
async def test_reload_calls_put_on_apps() -> None:
    """`reload()` → PUT /api/apps (reload from disk; no payload)."""
    _mock_preamble()
    route = respx.put("https://dhis2.example/api/apps").mock(return_value=httpx.Response(200))
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        await client.apps.reload()
    assert route.called


@respx.mock
async def test_hub_list_parses_catalog_rows() -> None:
    """GET /api/appHub → typed list[AppHubApp] with nested version records."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/appHub").mock(return_value=httpx.Response(200, json=_HUB_PAYLOAD))
    async with Dhis2Client("https://dhis2.example", auth=_auth()) as client:
        hub = await client.apps.hub_list()
    assert len(hub) == 1
    assert hub[0].id == "hub-widget-001"
    assert len(hub[0].versions) == 2
    assert hub[0].versions[0].version == "1.0.0"
