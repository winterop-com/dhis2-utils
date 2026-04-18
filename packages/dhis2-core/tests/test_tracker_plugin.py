"""Unit tests for the tracker plugin."""

from __future__ import annotations

from dhis2_core.plugins.tracker import plugin


def test_plugin_descriptor() -> None:
    assert plugin.name == "tracker"
    assert "tracker" in plugin.description.lower()
