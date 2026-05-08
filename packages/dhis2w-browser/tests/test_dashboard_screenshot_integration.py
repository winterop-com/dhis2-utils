"""Slow-marked integration test — seed stack captures into real PNG files."""

from __future__ import annotations

from pathlib import Path

import pytest
from dhis2w_core.plugins.browser.service import capture_dashboards
from dhis2w_core.profile import Profile
from PIL import Image

pytestmark = pytest.mark.slow


async def test_capture_dashboards_writes_valid_pngs(
    tmp_path: Path,
    local_url: str,
    local_username: str,
    local_password: str,
    local_available: bool,
) -> None:
    """End-to-end: seeded stack → Playwright → each dashboard → a non-empty PNG on disk."""
    if not local_available:
        pytest.skip(f"local DHIS2 not reachable at {local_url}")

    profile = Profile(
        base_url=local_url,
        auth="basic",
        username=local_username,
        password=local_password,
    )
    results = await capture_dashboards(
        profile,
        output_dir=tmp_path,
        headless=True,
    )
    assert results, "expected at least one dashboard capture against the seeded stack"
    for result in results:
        assert result.output_path.exists(), f"missing PNG for {result.display_name!r}"
        # Every capture must live under `{output_dir}/{instance-slug}/` —
        # namespace protects multi-stack runs from overwriting each other.
        assert result.output_path.parent.parent == tmp_path, (
            f"expected {result.output_path} to live under an instance-slug subdir of {tmp_path}"
        )
        assert result.output_path.stat().st_size > 5_000, (
            f"PNG suspiciously small for {result.display_name!r}: {result.output_path.stat().st_size} bytes"
        )
        image = Image.open(result.output_path)
        assert image.size[0] >= 1000, "expected wide-format capture"
        assert image.size[1] >= 200, "expected non-trivial height"
