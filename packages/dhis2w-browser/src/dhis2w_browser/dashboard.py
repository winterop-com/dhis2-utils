"""Full-page screenshot helpers for DHIS2 dashboards.

The DHIS2 dashboard app is a React SPA where each dashboard item loads its
own plugin iframe. Three quirks the helpers in this module paper over:

1. **Lazy-load via viewport intersection.** The app only materialises a
   plugin iframe when its slot scrolls into view. Programmatic `scrollTop`
   doesn't fire the intersection observers — real `mouse.wheel` events are
   required.

2. **Nested render detection.** There's no single "dashboard ready" event.
   The only reliable way to know an item has rendered is to poke the inner
   plugin iframe for substantial content (canvas / svg / leaflet /
   highcharts / img / long text). A plateau detector covers items that
   never fully render (data issues, bad expressions) so one stuck chart
   doesn't block the whole capture.

3. **Session-spanning hash navigation.** Switching dashboards via a fresh
   URL forces a full reload (re-auth, re-init). Setting
   `iframe.contentWindow.location.hash = '/{uid}'` swaps dashboards in
   place — saves 3+ seconds per capture on big batches.
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


class DashboardTarget(BaseModel):
    """One dashboard the caller wants captured — uid + display name + item count."""

    model_config = ConfigDict(frozen=True)

    uid: str
    display_name: str
    item_count: int


class CaptureResult(BaseModel):
    """Outcome of one dashboard capture — output file + render-completion stats."""

    model_config = ConfigDict(frozen=True)

    uid: str
    display_name: str
    output_path: Path
    items_expected: int
    items_rendered: int


def slugify(name: str) -> str:
    """Produce a filename-safe slug from a dashboard display name."""
    stripped = name.lower().strip()
    stripped = re.sub(r"[^\w\s-]", "", stripped)
    stripped = re.sub(r"[\s_-]+", "-", stripped)
    return stripped.strip("-") or "dashboard"


async def hide_chrome(page: Page) -> None:
    """Hide DHIS2's outer header + the inner dashboard-app toolbar via injected CSS.

    The header is on the outer page; the dashboard toolbar is inside the
    plugin-host iframe (DHIS2's apps are iframed off the apps shell).
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
        }"""
    )
    await page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe');
            if (!iframe || !iframe.contentDocument) return;
            const doc = iframe.contentDocument;
            const toolbar = doc.querySelector('[data-test="dashboard-bar"]')
                || doc.querySelector('div[class*="toolbar"]');
            if (toolbar) toolbar.style.display = 'none';
        }"""
    )


async def count_rendered_items(page: Page) -> int:
    """Count `.react-grid-item` slots whose inner plugin iframe has rendered content.

    "Rendered" = the inner iframe's body contains a canvas, an SVG with
    substantive paths/rects, a leaflet/highcharts container, or an image, or
    the body's innerText is non-trivial (long text items). Cross-origin
    inner iframes throw on `contentDocument` access — swallow those; they're
    either app-iframes we can't inspect or plugin fallbacks that don't
    matter for render detection.
    """
    raw = await page.evaluate(
        """() => {
            const outer = document.querySelector('iframe');
            if (!outer || !outer.contentDocument) return 0;
            const items = outer.contentDocument.querySelectorAll('.react-grid-item');
            let count = 0;
            items.forEach(el => {
                const inner = el.querySelector('iframe');
                if (!inner) {
                    // Items without an inner iframe (text blocks, etc.) — check the
                    // slot itself.
                    if (el.innerText.trim().length > 30) count++;
                    return;
                }
                try {
                    const doc = inner.contentDocument;
                    if (!doc || !doc.body) return;
                    const has = doc.querySelector('canvas')
                        || doc.querySelector('svg path')
                        || doc.querySelector('svg rect')
                        || doc.querySelector('table td')
                        || doc.querySelector('[class*="leaflet"]')
                        || doc.querySelector('[class*="highcharts"]')
                        || doc.querySelector('video')
                        || doc.querySelector('img[src]')
                        || doc.body.innerText.trim().length > 100;
                    if (has) count++;
                } catch {
                    // Cross-origin iframe — skip.
                }
            });
            return count;
        }"""
    )
    return int(raw) if isinstance(raw, (int, float)) else 0


async def wait_for_render(
    page: Page,
    expected: int,
    *,
    timeout_seconds: float = 90.0,
    poll_seconds: float = 2.0,
    plateau_polls: int = 3,
) -> int:
    """Block until `expected` items have rendered, or the count plateaus.

    Returns the highest `count_rendered_items(page)` result observed. The
    plateau detector gives up gracefully after `plateau_polls` consecutive
    unchanged polls — one stuck chart doesn't stall the rest of the pipeline.
    """
    deadline = asyncio.get_running_loop().time() + timeout_seconds
    rendered = 0
    stable_count = 0
    last_rendered = -1
    while asyncio.get_running_loop().time() < deadline:
        rendered = await count_rendered_items(page)
        if rendered >= expected:
            return rendered
        if rendered == last_rendered:
            stable_count += 1
            if stable_count >= plateau_polls:
                return rendered
        else:
            stable_count = 0
        last_rendered = rendered
        await asyncio.sleep(poll_seconds)
    return rendered


async def get_content_height(page: Page) -> int:
    """Measure the furthest `.react-grid-item.bottom` so the viewport sizes right."""
    height = await page.evaluate(
        """() => {
            const iframe = document.querySelector('iframe');
            if (!iframe || !iframe.contentDocument) return 2000;
            const items = iframe.contentDocument.querySelectorAll('.react-grid-item');
            let maxBottom = 0;
            items.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.bottom > maxBottom) maxBottom = rect.bottom;
            });
            return maxBottom || 2000;
        }"""
    )
    return int(height)


async def scroll_to_load_all_items(page: Page, *, steps: int = 20, step_pixels: int = 800) -> None:
    """Scroll through the dashboard with real `mouse.wheel` events to trigger lazy loading.

    Programmatic `scrollTop` doesn't fire DHIS2's intersection-observer hooks;
    only real wheel events prompt the app to materialise plugin iframes that
    are still offscreen. Clicks into the dashboard area first so the inner
    iframe has focus, scrolls down to the bottom, then back up so the first
    items are re-visible when the screenshot fires.
    """
    for _ in range(15):
        count = await page.evaluate(
            """() => {
                const f = document.querySelector('iframe');
                if (!f || !f.contentDocument) return 0;
                return f.contentDocument.querySelectorAll('.react-grid-item').length;
            }"""
        )
        if count > 0:
            break
        await asyncio.sleep(1)
    await page.mouse.click(700, 400)
    await asyncio.sleep(0.5)
    for _ in range(steps):
        await page.mouse.wheel(0, step_pixels)
        await asyncio.sleep(0.4)
    for _ in range(steps):
        await page.mouse.wheel(0, -step_pixels)
        await asyncio.sleep(0.15)
    await asyncio.sleep(2)


async def switch_dashboard(page: Page, dashboard_uid: str, *, settle_seconds: float = 5.0) -> None:
    """Swap the inner iframe's hash to the given dashboard UID — no full reload.

    The dashboard app reads the hash off its own location and re-renders in
    place, dropping the prior grid items and building new ones. Settling
    time gives the grid time to materialise before the caller starts
    checking render completion.
    """
    await page.evaluate(
        f"""() => {{
            const iframe = document.querySelector('iframe');
            if (iframe && iframe.contentWindow) {{
                iframe.contentWindow.location.hash = '/{dashboard_uid}';
            }}
        }}"""
    )
    await asyncio.sleep(settle_seconds)


def trim_background(path: Path) -> None:
    """Crop uniform-colour edges off the bottom + right of a screenshot (in-place)."""
    img = Image.open(path)
    pixels = img.load()
    if pixels is None:  # pragma: no cover — Pillow always returns PixelAccess for PNGs
        return
    width, height = img.size
    background = pixels[width - 1, height - 1]

    crop_y = height
    for y in range(height - 1, -1, -1):
        if not all(pixels[x, y] == background for x in range(0, width, 10)):
            crop_y = min(y + 20, height)
            break

    crop_x = width
    for x in range(width - 1, -1, -1):
        if not all(pixels[x, y] == background for y in range(0, crop_y, 10)):
            crop_x = min(x + 20, width)
            break

    if crop_x < width or crop_y < height:
        img.crop((0, 0, crop_x, crop_y)).save(path)


def add_banner(
    path: Path,
    dashboard_name: str,
    *,
    instance_url: str,
    username: str,
    item_count: int,
    timestamp: datetime | None = None,
) -> None:
    """Prepend a dark info banner above the screenshot (in-place)."""
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
    text = (
        f"  {dashboard_name}  |  {instance}  |  {item_count} items  |  {when.strftime('%Y-%m-%d %H:%M')}  |  {username}"
    )
    draw.text((10, 10), text, fill=(220, 225, 234), font=font)

    result = Image.new("RGB", (width, banner_height + height))
    result.paste(banner, (0, 0))
    result.paste(img.convert("RGB"), (0, banner_height))
    result.save(path)


async def capture_dashboard(
    page: Page,
    target: DashboardTarget,
    output_path: Path,
    *,
    viewport_width: int = 1400,
    viewport_height_expanded: int = 8000,
    render_timeout_seconds: float = 90.0,
) -> CaptureResult:
    """Screenshot one dashboard, assuming `page` is already on the dashboard app.

    Caller handles switching between dashboards (via `switch_dashboard`) or
    initial navigation. This function handles: reset viewport → scroll-trigger
    lazy loads → wait for renders → resize viewport to fit content → hide
    chrome → capture full page.
    """
    await page.set_viewport_size({"width": viewport_width, "height": 900})

    if target.item_count == 0:
        # Empty dashboard — skip the scroll+wait dance; just hide chrome + snap.
        await hide_chrome(page)
        await page.screenshot(path=str(output_path), full_page=True)
        return CaptureResult(
            uid=target.uid,
            display_name=target.display_name,
            output_path=output_path,
            items_expected=0,
            items_rendered=0,
        )

    await scroll_to_load_all_items(page)
    await page.set_viewport_size({"width": viewport_width, "height": viewport_height_expanded})
    await asyncio.sleep(3)

    rendered = await wait_for_render(page, target.item_count, timeout_seconds=render_timeout_seconds)

    content_height = await get_content_height(page) + 50
    await page.set_viewport_size({"width": viewport_width, "height": content_height})
    await asyncio.sleep(2)

    await hide_chrome(page)
    await page.screenshot(path=str(output_path), full_page=True)
    return CaptureResult(
        uid=target.uid,
        display_name=target.display_name,
        output_path=output_path,
        items_expected=target.item_count,
        items_rendered=rendered,
    )
