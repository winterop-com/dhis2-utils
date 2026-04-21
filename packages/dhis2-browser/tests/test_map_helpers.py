"""Unit tests for pure helpers in `dhis2_browser.maps`."""

from __future__ import annotations

from pathlib import Path

from dhis2_browser.maps import add_map_banner, slugify_map
from PIL import Image


def test_slugify_map_standard_names() -> None:
    assert slugify_map("OPD consultations — 2024 choropleth") == "opd-consultations-2024-choropleth"
    assert slugify_map("  mixed   WHITESPACE   ") == "mixed-whitespace"


def test_slugify_map_never_returns_empty_string() -> None:
    assert slugify_map("") == "map"
    assert slugify_map("!!! --- !!!") == "map"


def test_add_map_banner_prepends_info_strip(tmp_path: Path) -> None:
    path = tmp_path / "probe.png"
    Image.new("RGB", (400, 200), (255, 255, 255)).save(path)
    add_map_banner(path, "Probe map", instance_url="http://localhost:8080", username="admin", layer_count=2)
    output = Image.open(path)
    assert output.size == (400, 236)
    pixel = output.getpixel((2, 2))
    assert isinstance(pixel, tuple)
    assert pixel[:3] == (55, 63, 81)


def test_add_map_banner_handles_singular_layer_label(tmp_path: Path) -> None:
    path = tmp_path / "probe2.png"
    Image.new("RGB", (300, 150), (255, 255, 255)).save(path)
    # layer_count=1 uses "1 layer" (singular); 0 or None omits the label.
    add_map_banner(path, "Single-layer", instance_url="http://localhost:8080", username="admin", layer_count=1)
    assert Image.open(path).size == (300, 186)
