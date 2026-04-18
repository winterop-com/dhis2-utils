"""Unit tests for the analytics plugin."""

from __future__ import annotations

from dhis2_core.plugins.analytics import plugin


def test_plugin_descriptor() -> None:
    assert plugin.name == "analytics"
    assert "analytics" in plugin.description.lower()
