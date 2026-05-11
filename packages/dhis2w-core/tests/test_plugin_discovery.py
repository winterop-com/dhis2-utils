"""Unit tests for dhis2w-core plugin discovery."""

from __future__ import annotations

from dhis2w_core.plugin import discover_plugins


def test_discover_plugins_includes_system() -> None:
    """Discover plugins includes system."""
    plugins = discover_plugins()
    names = {plugin.name for plugin in plugins}
    assert "system" in names


def test_system_plugin_has_cli_and_mcp_registrars() -> None:
    """System plugin has cli and mcp registrars."""
    plugins = {plugin.name: plugin for plugin in discover_plugins()}
    system = plugins["system"]
    assert callable(system.register_cli)
    assert callable(system.register_mcp)
    assert system.description
