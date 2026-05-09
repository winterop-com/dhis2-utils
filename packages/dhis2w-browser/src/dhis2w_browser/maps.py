"""Single-map screenshot helpers — `capture_map`.

DHIS2 Maps render in the Maps app (`/dhis-web-maps/#/<uid>` → `/apps/maps`
on v42+) via MapLibre GL — a vector-map library that renders to a
`<canvas>` with lots of `<svg>` overlays for legends and controls.
`capture_map` mirrors the visualization-screenshot path: navigate,
wait for the canvas + MapLibre classes to appear, hide outer DHIS2
chrome, write a full-page PNG.

Same rendering-detection loop as the viz capture: look through the
inner iframe for substantive content (canvas / MapLibre classes /
SVG paths) with a plateau detector so a broken map doesn't stall
the batch.
"""

from __future__ import annotations

import asyncio
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from playwright.async_api import Page


class MapTarget(BaseModel):
    """One Map to capture — uid + display name for the banner + filename."""

    model_config = ConfigDict(frozen=True)

    uid: str
    display_name: str


class MapCaptureResult(BaseModel):
    """Outcome of one map capture — output file + rendered flag."""

    model_config = ConfigDict(frozen=True)

    uid: str
    display_name: str
    output_path: Path
    rendered: bool


async def _hide_map_chrome(page: Page) -> None:
    """Hide the outer DHIS2 header + any inner Maps toolbar."""
    await page.evaluate(
        """() => {
            const header = document.querySelector('header');
            if (header) header.style.display = 'none';
            const iframe = document.querySelector('iframe');
            if (iframe) {
                iframe.style.top = '0';
                iframe.style.height = '100vh';
            }
        }""",
    )
    await page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe');
            if (!iframe || !iframe.contentDocument) return;
            const doc = iframe.contentDocument;
            const suspects = [
                '[data-test="app-titlebar"]',
                '[data-test="dhis2-app-menu"]',
                '[class*="AppTitle"]',
                '[class*="MenuBar"]',
                'nav',
            ];
            suspects.forEach(sel => {
                doc.querySelectorAll(sel).forEach(el => { el.style.display = 'none'; });
            });
        }""",
    )


async def _has_rendered_map(page: Page) -> bool:
    """True when the inner iframe has a rendered map canvas."""
    result = await page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe');
            if (!iframe || !iframe.contentDocument) return false;
            const doc = iframe.contentDocument;
            if (!doc.body) return false;
            // MapLibre / Leaflet canvases signal a map that's painted.
            return Boolean(
                doc.querySelector('canvas.maplibregl-canvas')
                || doc.querySelector('[class*="maplibre"]')
                || doc.querySelector('[class*="leaflet"]')
                || doc.querySelector('canvas')
                || doc.body.innerText.trim().length > 100,
            );
        }""",
    )
    return bool(result)


async def _wait_for_map_render(
    page: Page,
    *,
    timeout_seconds: float = 60.0,
    poll_seconds: float = 1.0,
) -> bool:
    """Block until the map renders or `timeout_seconds` elapses."""
    deadline = asyncio.get_running_loop().time() + timeout_seconds
    while asyncio.get_running_loop().time() < deadline:
        if await _has_rendered_map(page):
            return True
        await asyncio.sleep(poll_seconds)
    return await _has_rendered_map(page)


def slugify_map(name: str) -> str:
    """Produce a filename-safe slug from a map display name."""
    stripped = name.lower().strip()
    stripped = re.sub(r"[^\w\s-]", "", stripped)
    stripped = re.sub(r"[\s_-]+", "-", stripped)
    return stripped.strip("-") or "map"


async def capture_map(
    page: Page,
    target: MapTarget,
    output_path: Path,
    *,
    viewport_width: int = 1400,
    viewport_height: int = 900,
    render_timeout_seconds: float = 60.0,
    tile_settle_seconds: float = 3.0,
) -> MapCaptureResult:
    """Screenshot one Map assuming `page` is already on the Maps app.

    The basemap tiles and vector overlays animate in — after the initial
    render detection, wait an extra `tile_settle_seconds` so the tiles
    fully paint before the screenshot fires.
    """
    await page.set_viewport_size({"width": viewport_width, "height": viewport_height})
    rendered = await _wait_for_map_render(page, timeout_seconds=render_timeout_seconds)
    # Tiles + legends fade in; wait a bit more so the screenshot isn't mid-animation.
    await asyncio.sleep(tile_settle_seconds)
    await _hide_map_chrome(page)
    await asyncio.sleep(1)
    await page.screenshot(path=str(output_path), full_page=True)
    return MapCaptureResult(
        uid=target.uid,
        display_name=target.display_name,
        output_path=output_path,
        rendered=rendered,
    )


def add_map_banner(
    path: Path,
    display_name: str,
    *,
    instance_url: str,
    username: str,
    layer_count: int | None = None,
    timestamp: datetime | None = None,
) -> None:
    """Prepend a dark info banner above the map screenshot (in-place)."""
    when = timestamp or datetime.now(tz=UTC)
    img = Image.open(path)
    width, height = img.size

    banner_height = 36
    banner = Image.new("RGB", (width, banner_height), (55, 63, 81))
    draw = ImageDraw.Draw(banner)

    font: ImageFont.ImageFont | ImageFont.FreeTypeFont
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 14)
    except OSError:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
        except OSError:
            font = ImageFont.load_default()

    instance = re.sub(r"https?://", "", instance_url)
    layer_label = f"  |  {layer_count} layer{'s' if layer_count != 1 else ''}" if layer_count is not None else ""
    text = f"  {display_name}{layer_label}  |  {instance}  |  {when.strftime('%Y-%m-%d %H:%M')}  |  {username}"
    draw.text((10, 10), text, fill=(220, 225, 234), font=font)

    result = Image.new("RGB", (width, banner_height + height))
    result.paste(banner, (0, 0))
    result.paste(img.convert("RGB"), (0, banner_height))
    result.save(path)


__all__ = [
    "MapCaptureResult",
    "MapTarget",
    "add_map_banner",
    "capture_map",
    "slugify_map",
]
