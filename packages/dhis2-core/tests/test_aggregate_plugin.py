"""Unit tests for the aggregate plugin."""

from __future__ import annotations

from dhis2_core.plugins.aggregate import plugin


def test_plugin_descriptor() -> None:
    assert plugin.name == "aggregate"
    assert "aggregate" in plugin.description.lower()
