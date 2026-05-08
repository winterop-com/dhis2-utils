"""Unit tests for the data plugin (aggregate + tracker sub-groups)."""

from __future__ import annotations

from dhis2w_core.plugins.data import plugin


def test_plugin_descriptor() -> None:
    assert plugin.name == "data"
    assert "aggregate" in plugin.description.lower()
    assert "tracker" in plugin.description.lower()
