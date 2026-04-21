"""Multi-line time-series — one line per org unit, months on the x-axis.

This is the canonical "trend by region" chart shape. `LINE`'s default
placement (`rows=[pe]`, `columns=[ou]`, `filters=[dx]`) already maps
time to the x-axis and provinces to the series, so the spec stays
tiny.

Usage:
    uv run python examples/client/viz_multiline_by_province.py
"""

from __future__ import annotations

from _runner import run_example
from dhis2_client import VisualizationSpec
from dhis2_client.generated.v42.enums import VisualizationType
from dhis2_core.client_context import open_client
from dhis2_core.profile import profile_from_env

VIZ_UID = "VizExMulti1"
PROVINCES = ["NORNordland", "NOROsloProv", "NORTrondlag", "NORVestland"]
MONTHS_2024 = [f"2024{m:02d}" for m in range(1, 13)]


async def main() -> None:
    """Multi-line ANC chart: 4 provinces × 12 months."""
    async with open_client(profile_from_env()) as client:
        # First sanity-check: analytics must return non-zero values before
        # a chart will render anything useful. Pull one period as a probe.
        probe = await client.get_raw(
            "/api/analytics",
            params={
                "dimension": ["dx:DEancVisit1", "pe:202406", f"ou:{';'.join(PROVINCES)}"],
                "skipMeta": "true",
            },
        )
        rows = probe.get("rows") or []
        if not rows:
            raise RuntimeError("analytics returned zero rows — run `dhis2 maintenance refresh-analytics`")
        print(f"[analytics probe] 202406 rows={len(rows)} (non-zero, safe to render)")

        spec = VisualizationSpec(
            name="Example: ANC monthly by province (2024)",
            viz_type=VisualizationType.LINE,
            data_elements=["DEancVisit1"],
            periods=MONTHS_2024,
            organisation_units=PROVINCES,
            uid=VIZ_UID,
        )
        viz = await client.visualizations.create_from_spec(spec)
        print(f"[created] {viz.id}  series={viz.columnDimensions}  category={viz.rowDimensions}")

        await client.visualizations.delete(VIZ_UID)
        print("[deleted]")


if __name__ == "__main__":
    run_example(main)
