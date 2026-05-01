"""Respx-mocked tests for `Dhis2Client.customize` — assert the wire contract DHIS2 v42 actually needs."""

from __future__ import annotations

import httpx
import pytest
import respx
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.customize import LoginCustomization


@pytest.fixture
def client() -> Dhis2Client:
    """Build a client with a pre-primed HTTP pool (skips connect / version discovery)."""
    instance = Dhis2Client(
        "https://dhis2.example",
        auth=BasicAuth(username="admin", password="district"),
    )
    instance._http = httpx.AsyncClient(base_url="https://dhis2.example")
    return instance


@respx.mock
async def test_upload_logo_front_sends_multipart_and_flips_flag(client: Dhis2Client) -> None:
    """Upload posts a multipart to /api/staticContent/logo_front AND flips keyUseCustomLogoFront=true.

    The flag flip is load-bearing — without it, DHIS2 redirects GETs back to the
    built-in default (BUGS.md entry 11).
    """
    upload = respx.post("https://dhis2.example/api/staticContent/logo_front").mock(
        return_value=httpx.Response(204),
    )
    flag = respx.post("https://dhis2.example/api/systemSettings/keyUseCustomLogoFront").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    try:
        await client.customize.upload_logo_front(b"\x89PNG\r\n\x1a\n fake", filename="front.png")
    finally:
        await client.close()
    assert upload.called
    assert flag.called
    # Upload must be multipart/form-data with a `file` field.
    body = upload.calls.last.request.content
    assert b'name="file"' in body
    assert b'filename="front.png"' in body
    # Flag value is "true" as text/plain.
    assert flag.calls.last.request.content == b"true"
    assert flag.calls.last.request.headers["content-type"] == "text/plain"


@respx.mock
async def test_upload_logo_banner_flips_its_own_flag(client: Dhis2Client) -> None:
    """logo_banner upload must flip keyUseCustomLogoBanner (different setting from logo_front)."""
    upload = respx.post("https://dhis2.example/api/staticContent/logo_banner").mock(
        return_value=httpx.Response(204),
    )
    flag = respx.post("https://dhis2.example/api/systemSettings/keyUseCustomLogoBanner").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    try:
        await client.customize.upload_logo_banner(b"banner bytes")
    finally:
        await client.close()
    assert upload.called
    assert flag.called


@respx.mock
async def test_upload_style_posts_css_and_sets_keystyle(client: Dhis2Client) -> None:
    """CSS upload goes to /api/files/style as text/css + sets keyStyle=style to activate it."""
    upload = respx.post("https://dhis2.example/api/files/style").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    flag = respx.post("https://dhis2.example/api/systemSettings/keyStyle").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    try:
        await client.customize.upload_style("body { color: red; }")
    finally:
        await client.close()
    assert upload.called
    assert upload.calls.last.request.headers["content-type"] == "text/css"
    assert upload.calls.last.request.content == b"body { color: red; }"
    assert flag.calls.last.request.content == b"style"


@respx.mock
async def test_set_system_setting_uses_text_plain(client: Dhis2Client) -> None:
    """DHIS2's system-setting endpoint needs a text/plain body, not JSON."""
    route = respx.post("https://dhis2.example/api/systemSettings/applicationTitle").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    try:
        await client.customize.set_system_setting("applicationTitle", "My DHIS2")
    finally:
        await client.close()
    assert route.called
    assert route.calls.last.request.headers["content-type"] == "text/plain"
    assert route.calls.last.request.content == b"My DHIS2"


@respx.mock
async def test_apply_preset_runs_every_stage_in_order(client: Dhis2Client) -> None:
    """apply_preset: logos → style → settings, returning a summary of what happened."""
    respx.post("https://dhis2.example/api/staticContent/logo_front").mock(return_value=httpx.Response(204))
    respx.post("https://dhis2.example/api/staticContent/logo_banner").mock(return_value=httpx.Response(204))
    respx.post("https://dhis2.example/api/files/style").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    # 3 keyUse* + keyStyle flips + 2 user settings
    respx.post(url__regex=r"https://dhis2\.example/api/systemSettings/.*").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    preset = LoginCustomization(
        logo_front=b"front",
        logo_banner=b"banner",
        style_css="body{}",
        system_settings={"applicationTitle": "t", "keyApplicationFooter": "f"},
    )
    try:
        result = await client.customize.apply_preset(preset)
    finally:
        await client.close()
    assert result.logo_front_uploaded
    assert result.logo_banner_uploaded
    assert result.style_uploaded
    assert result.settings_applied == ["applicationTitle", "keyApplicationFooter"]


@respx.mock
async def test_apply_empty_preset_is_a_no_op(client: Dhis2Client) -> None:
    """An empty preset doesn't hit the network — useful for gating on env toggles."""
    try:
        result = await client.customize.apply_preset(LoginCustomization())
    finally:
        await client.close()
    assert not result.logo_front_uploaded
    assert not result.logo_banner_uploaded
    assert not result.style_uploaded
    assert result.settings_applied == []


@respx.mock
async def test_get_login_config_hits_the_read_only_endpoint(client: Dhis2Client) -> None:
    """Regression: don't accidentally read from /api/systemSettings."""
    route = respx.get("https://dhis2.example/api/loginConfig").mock(
        return_value=httpx.Response(200, json={"applicationTitle": "dhis2-utils local"}),
    )
    try:
        config = await client.customize.get_login_config()
    finally:
        await client.close()
    assert route.called
    assert config.applicationTitle == "dhis2-utils local"
