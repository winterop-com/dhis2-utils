"""Unit tests for the FastAPI-backed OAuth2 redirect receiver."""

from __future__ import annotations

import asyncio
import socket

import httpx
import pytest
from dhis2_client.errors import OAuth2FlowError
from dhis2_core.oauth2_redirect import capture_code


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port: int = s.getsockname()[1]
        return port


async def _fire_redirect(url: str, *, max_tries: int = 30) -> None:
    """Hit `url` once the server is up; retries a few times on ConnectError."""
    last_err: Exception | None = None
    for _ in range(max_tries):
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                await client.get(url)
            return
        except httpx.ConnectError as exc:
            last_err = exc
            await asyncio.sleep(0.05)
    if last_err is not None:
        raise last_err


async def test_capture_happy_path() -> None:
    port = _free_port()
    redirect_uri = f"http://127.0.0.1:{port}/"
    fire = asyncio.create_task(_fire_redirect(f"{redirect_uri}?code=abc123&state=expected-state"))
    try:
        code = await capture_code(redirect_uri, "expected-state", timeout=10.0)
    finally:
        await fire
    assert code == "abc123"


async def test_capture_state_mismatch_raises() -> None:
    port = _free_port()
    redirect_uri = f"http://127.0.0.1:{port}/"
    fire = asyncio.create_task(_fire_redirect(f"{redirect_uri}?code=abc&state=wrong"))
    try:
        with pytest.raises(OAuth2FlowError, match="state mismatch"):
            await capture_code(redirect_uri, "right", timeout=10.0)
    finally:
        await fire


async def test_capture_error_param_raises() -> None:
    port = _free_port()
    redirect_uri = f"http://127.0.0.1:{port}/"
    fire = asyncio.create_task(_fire_redirect(f"{redirect_uri}?error=access_denied&error_description=user+declined"))
    try:
        with pytest.raises(OAuth2FlowError, match="authorization failed"):
            await capture_code(redirect_uri, "expected-state", timeout=10.0)
    finally:
        await fire


async def test_capture_timeout_raises() -> None:
    port = _free_port()
    redirect_uri = f"http://127.0.0.1:{port}/"
    with pytest.raises(OAuth2FlowError, match="no OAuth2 redirect received"):
        await capture_code(redirect_uri, "expected-state", timeout=0.5)
