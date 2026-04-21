"""Single-visualization screenshot helpers — `capture_visualization`.

DHIS2 has no native `/api/visualizations/{uid}.png` endpoint. Chart
rendering happens client-side in the Data Visualizer React app, which
is iframed off the apps shell. Navigating to
`/dhis-web-data-visualizer/#/<uid>` (redirected to
`/apps/data-visualizer#/<uid>` on v42+) loads the chart inside a plugin
iframe; SVG / canvas / table elements appear once rendering is done.

Two quirks to paper over:

1. **Render detection through an inner iframe.** Same pattern as the
   dashboard-app capture path: `iframe.contentDocument.querySelector`
   for substantive content (SVG path, table td, `.highcharts-container`,
   canvas, long text). A plateau detector gives up gracefully if the
   chart never fully materialises.

2. **Data Visualizer chrome dominates the page.** The app ships with a
   top toolbar, left dimension picker, and sometimes a right layout
   panel. For a clean PNG we hide the outer DHIS2 header and any
   inner toolbar; the `trim_background` helper shared with the
   dashboard path crops uniform-background whitespace afterwards.
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


class VisualizationTarget(BaseModel):
    """One Visualization to capture — uid + display name for the banner + filename."""

    model_config = ConfigDict(frozen=True)

    uid: str
    display_name: str
    viz_type: str | None = None


class VisualizationCaptureResult(BaseModel):
    """Outcome of one viz capture — output file + rendered flag."""

    model_config = ConfigDict(frozen=True)

    uid: str
    display_name: str
    output_path: Path
    rendered: bool


async def _hide_viz_chrome(page: Page) -> None:
    """Hide the outer DHIS2 header + any inner Data Visualizer toolbar.

    The outer header lives on `page`; the Data Visualizer toolbar is
    inside the plugin iframe. Both are injected via `page.evaluate` so
    they apply regardless of build version.
    """
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
            // Hide the Data Visualizer app toolbar / menu bar — best-effort
            // selectors so we tolerate DHIS2 UI refreshes.
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


async def _has_rendered_chart(page: Page) -> bool:
    """True when the inner iframe has substantive visualization content."""
    result = await page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe');
            if (!iframe || !iframe.contentDocument) return false;
            const doc = iframe.contentDocument;
            if (!doc.body) return false;
            return Boolean(
                doc.querySelector('.highcharts-container')
                || doc.querySelector('canvas')
                || doc.querySelector('svg path')
                || doc.querySelector('svg rect')
                || doc.querySelector('table td')
                || doc.querySelector('[class*="leaflet"]')
                || doc.body.innerText.trim().length > 100,
            );
        }""",
    )
    return bool(result)


async def _wait_for_chart_render(
    page: Page,
    *,
    timeout_seconds: float = 45.0,
    poll_seconds: float = 1.0,
) -> bool:
    """Block until the chart renders or `timeout_seconds` elapses."""
    deadline = asyncio.get_event_loop().time() + timeout_seconds
    while asyncio.get_event_loop().time() < deadline:
        if await _has_rendered_chart(page):
            return True
        await asyncio.sleep(poll_seconds)
    return await _has_rendered_chart(page)


def slugify_viz(name: str) -> str:
    """Produce a filename-safe slug from a visualization display name."""
    stripped = name.lower().strip()
    stripped = re.sub(r"[^\w\s-]", "", stripped)
    stripped = re.sub(r"[\s_-]+", "-", stripped)
    return stripped.strip("-") or "visualization"


async def capture_visualization(
    page: Page,
    target: VisualizationTarget,
    output_path: Path,
    *,
    viewport_width: int = 1400,
    viewport_height: int = 900,
    render_timeout_seconds: float = 45.0,
) -> VisualizationCaptureResult:
    """Screenshot one Visualization assuming `page` is already on the viz app.

    Caller navigates to `/dhis-web-data-visualizer/#/<uid>` (via
    `authenticated_session(..., navigate_to=...)`) before calling this.
    The function blocks until the chart renders (or the plateau detector
    gives up), hides chrome, and writes a full-page PNG.
    """
    await page.set_viewport_size({"width": viewport_width, "height": viewport_height})
    rendered = await _wait_for_chart_render(page, timeout_seconds=render_timeout_seconds)
    await _hide_viz_chrome(page)
    await asyncio.sleep(1)
    await page.screenshot(path=str(output_path), full_page=True)
    return VisualizationCaptureResult(
        uid=target.uid,
        display_name=target.display_name,
        output_path=output_path,
        rendered=rendered,
    )


def add_viz_banner(
    path: Path,
    display_name: str,
    *,
    instance_url: str,
    username: str,
    viz_type: str | None = None,
    timestamp: datetime | None = None,
) -> None:
    """Prepend a dark info banner above the viz screenshot (in-place)."""
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
    type_label = f"  |  {viz_type}" if viz_type else ""
    text = f"  {display_name}{type_label}  |  {instance}  |  {when.strftime('%Y-%m-%d %H:%M')}  |  {username}"
    draw.text((10, 10), text, fill=(220, 225, 234), font=font)

    result = Image.new("RGB", (width, banner_height + height))
    result.paste(banner, (0, 0))
    result.paste(img.convert("RGB"), (0, banner_height))
    result.save(path)


__all__ = [
    "VisualizationCaptureResult",
    "VisualizationTarget",
    "add_viz_banner",
    "capture_visualization",
    "slugify_viz",
]
