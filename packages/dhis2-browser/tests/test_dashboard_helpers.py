"""Unit tests for pure helpers in `dhis2_browser.dashboard` (no Playwright needed)."""

from __future__ import annotations

from pathlib import Path

from dhis2_browser.dashboard import add_banner, slugify, trim_background
from PIL import Image


def test_slugify_handles_typical_names() -> None:
    """Standard dashboard names → lowercase, hyphenated, no special chars."""
    assert slugify("Norway — Health services overview") == "norway-health-services-overview"
    assert slugify("ANC 1st visits") == "anc-1st-visits"
    assert slugify("  lots   of   whitespace  ") == "lots-of-whitespace"
    assert slugify("already-slug-like") == "already-slug-like"


def test_slugify_never_returns_empty_string() -> None:
    """An input stripped to nothing must still produce a usable filename."""
    assert slugify("") == "dashboard"
    assert slugify("!!! --- !!!") == "dashboard"


def test_trim_background_crops_uniform_edges(tmp_path: Path) -> None:
    """Uniform-colour bottom/right margins get cropped; content bbox stays."""
    # 200x200 with a 50x50 coloured square at top-left; rest is background.
    image = Image.new("RGB", (200, 200), (255, 255, 255))
    for y in range(50):
        for x in range(50):
            image.putpixel((x, y), (10, 10, 10))
    path = tmp_path / "probe.png"
    image.save(path)

    trim_background(path)

    cropped = Image.open(path)
    # Content occupies only the top-left; expect the crop to shrink both axes.
    assert cropped.size[0] < 200
    assert cropped.size[1] < 200
    # Content stays intact — top-left pixel should still be the dark square.
    assert cropped.getpixel((0, 0)) == (10, 10, 10)


def test_add_banner_prepends_height(tmp_path: Path) -> None:
    """Banner adds a fixed 36-px strip at the top; width stays the same."""
    image = Image.new("RGB", (400, 200), (128, 128, 128))
    path = tmp_path / "probe.png"
    image.save(path)

    add_banner(
        path,
        "Dashboard name",
        instance_url="https://dhis2.example",
        username="admin",
        item_count=3,
    )

    annotated = Image.open(path)
    assert annotated.size == (400, 236)  # 200 + 36
