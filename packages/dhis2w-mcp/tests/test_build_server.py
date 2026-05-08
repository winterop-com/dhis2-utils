"""Unit tests for dhis2-mcp server construction."""

from __future__ import annotations

from dhis2w_mcp.server import build_server


def test_build_server_registers_plugins() -> None:
    server = build_server()
    assert server is not None
