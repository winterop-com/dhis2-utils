"""Unit tests for pure helpers in `dhis2w_browser.visualization` (no Playwright needed)."""

from __future__ import annotations

from pathlib import Path

from dhis2w_browser.visualization import add_viz_banner, slugify_viz
from PIL import Image


def test_slugify_viz_handles_typical_names() -> None:
    """Visualization names → lowercase, hyphenated, no special characters."""
    assert slugify_viz("ANC 1st visits — monthly by province (2024)") == "anc-1st-visits-monthly-by-province-2024"
    assert slugify_viz("OPD consultations") == "opd-consultations"
    assert slugify_viz("   mixed   WHITESPACE   ") == "mixed-whitespace"


def test_slugify_viz_never_returns_empty_string() -> None:
    """An input stripped to nothing must still produce a usable filename."""
    assert slugify_viz("") == "visualization"
    assert slugify_viz("!!! --- !!!") == "visualization"


def test_add_viz_banner_prepends_info_strip(tmp_path: Path) -> None:
    """Banner render adds a 36-pixel strip above the captured chart."""
    input_path = tmp_path / "probe.png"
    Image.new("RGB", (400, 200), (255, 255, 255)).save(input_path)

    add_viz_banner(
        input_path,
        "Smoke viz",
        instance_url="http://localhost:8080",
        username="admin",
        viz_type="LINE",
    )

    output = Image.open(input_path)
    assert output.size == (400, 236)  # 200 + 36 banner
    # Top-left pixel is the banner background colour (55, 63, 81).
    pixel = output.getpixel((2, 2))
    assert isinstance(pixel, tuple)
    assert pixel[:3] == (55, 63, 81)


def test_add_viz_banner_omits_type_label_when_none(tmp_path: Path) -> None:
    """`viz_type=None` keeps the banner render alive (no crash)."""
    input_path = tmp_path / "probe2.png"
    Image.new("RGB", (300, 150), (255, 255, 255)).save(input_path)
    add_viz_banner(
        input_path,
        "No-type viz",
        instance_url="http://localhost:8080",
        username="admin",
        viz_type=None,
    )
    assert Image.open(input_path).size == (300, 186)
