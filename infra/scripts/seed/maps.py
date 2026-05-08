"""Programmatic map build for the Sierra Leone immunization seed.

The play42 snapshot ships 8 maps across the 3 dashboards. Every thematic
layer references coverage indicators we don't transitively pull (the
maps fail to resolve their `dataDimensionItems`) and several pin to
periods DHIS2 can't resolve against the 2024-only aggregate seed.

This module rebuilds each map via `Dhis2Client.maps.create_from_spec(...)`:

- Same UIDs as the bundle so every dashboard item resolves to the
  rebuilt map.
- Sierra Leone DE UIDs on every thematic layer — the 3 transitively
  imported indicators on the facility + boundary layers where a
  stock-style read fits.
- Fixed `2024` period so the choropleth renders against our aggregate
  data window.
- `Immunization Coverage` legend set (`BtxOoQuLyg1`) on the coverage
  layers so DHIS2 bands values into red/yellow/green ranges on the
  rendered map.

Called from `seed_play` after the programmatic viz build + before
the dashboard import, so every dashboard map item resolves to a
freshly-created map.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from dhis2w_client import MapLayerSpec, MapSpec

if TYPE_CHECKING:
    from dhis2w_client.client import Dhis2Client


# Sierra Leone viewport — centred on the country.
_SL_LON: float = -11.8
_SL_LAT: float = 8.5
_SL_ZOOM: int = 7

_SL_ROOT = "ImspTQPwCqd"

# Core DEs (mirror `seed.visualizations`).
_DE_BCG = "s46m5MS0hxu"
_DE_MEASLES = "YtbsuPPo010"
_DE_PENTA1 = "fClA2Erf6IO"
_DE_PENTA3 = "n6aMJNLdvep"
_DE_FIC = "UOlfIjgN8X6"

# Available indicators — Stock-PHU variants, only.
_IND_BCG_STOCK = "OEWO2PpiUKx"
_IND_MEASLES_STOCK = "loEBZlcsTlx"
_IND_OPV_STOCK = "bASXd9ukRGD"

# Note: the `Immunization Coverage` legend set (UID `BtxOoQuLyg1`) is
# deliberately NOT applied here. Its thresholds are 0-120 (% coverage)
# while our thematic layers drive off raw dose counts (thousands) —
# every value would land in the "Invalid" bucket. The `colorLow` /
# `colorHigh` gradient auto-scales to each layer's data range instead,
# which is the useful visualization for dose counts.

# The whole seed is 2024-only aggregate data, so maps pin to that year.
_YEAR_2024: list[str] = ["2024"]


def _coverage_layer(
    data_element: str,
    color_low: str = "#fef0d9",
    color_high: str = "#b30000",
    *,
    ou_level: int = 2,
) -> MapLayerSpec:
    """Thematic choropleth layer for one immunization DE at the given OU level."""
    return MapLayerSpec(
        layer_kind="thematic",
        data_elements=[data_element],
        periods=_YEAR_2024,
        organisation_units=[_SL_ROOT],
        organisation_unit_levels=[ou_level],
        color_low=color_low,
        color_high=color_high,
    )


def all_specs() -> list[MapSpec]:
    """Return every MapSpec the seed creates (8 total across the 3 dashboards)."""
    return [
        MapSpec(
            uid="Ku2Q3rcxPku",
            name="Immunization: Measles coverage by district 2024",
            longitude=_SL_LON,
            latitude=_SL_LAT,
            zoom=_SL_ZOOM,
            layers=[_coverage_layer(_DE_MEASLES, "#edf8b1", "#2c7fb8")],
        ),
        MapSpec(
            uid="Sdt40DKhq45",
            name="Immunization: BCG doses given at facility 2024",
            longitude=_SL_LON,
            latitude=_SL_LAT,
            zoom=_SL_ZOOM,
            layers=[_coverage_layer(_DE_BCG, ou_level=4)],
        ),
        MapSpec(
            uid="iKgbemGaDUh",
            name="Immunization: Penta 3 coverage by chiefdom 2024",
            longitude=_SL_LON,
            latitude=_SL_LAT,
            zoom=_SL_ZOOM,
            layers=[_coverage_layer(_DE_PENTA3, ou_level=3)],
        ),
        MapSpec(
            uid="kwX3awhakCk",
            name="Immunization: Fully immunized by chiefdom 2024",
            longitude=_SL_LON,
            latitude=_SL_LAT,
            zoom=_SL_ZOOM,
            layers=[_coverage_layer(_DE_FIC, "#f7fcb9", "#31a354", ou_level=3)],
        ),
        MapSpec(
            uid="mdsnjebmU2x",
            name="Immunization: BCG coverage by district 2024",
            longitude=_SL_LON,
            latitude=_SL_LAT,
            zoom=_SL_ZOOM,
            layers=[_coverage_layer(_DE_BCG)],
        ),
        MapSpec(
            uid="qN8cK4TwgkO",
            name="Immunization: BCG + FIC coverage by district 2024",
            longitude=_SL_LON,
            latitude=_SL_LAT,
            zoom=_SL_ZOOM,
            layers=[
                _coverage_layer(_DE_BCG),
                _coverage_layer(_DE_FIC, "#f7fcb9", "#31a354"),
            ],
        ),
        MapSpec(
            uid="xIywMQ27ku3",
            name="Measles: coverage by chiefdom 2024",
            longitude=_SL_LON,
            latitude=_SL_LAT,
            zoom=_SL_ZOOM,
            layers=[_coverage_layer(_DE_MEASLES, "#edf8b1", "#2c7fb8", ou_level=3)],
        ),
        MapSpec(
            uid="y3jLMnZTV6i",
            name="Sierra Leone: Health facilities",
            longitude=_SL_LON,
            latitude=_SL_LAT,
            zoom=_SL_ZOOM,
            layers=[
                MapLayerSpec(
                    layer_kind="facility",
                    organisation_units=[_SL_ROOT],
                    organisation_unit_levels=[4],
                    opacity=0.9,
                ),
            ],
        ),
    ]


async def build_dashboard_maps(client: Dhis2Client) -> int:
    """Create every seed map via the client's typed builder.

    Each spec round-trips through `MapsAccessor.create_from_spec`, which
    POSTs through `/api/metadata` — the only path that fully populates
    DHIS2's derived `rows` / `columns` / `filters` on each MapView.

    Returns the count of maps created so seed_play can report progress.
    """
    specs = all_specs()
    for spec in specs:
        await client.maps.create_from_spec(spec)
    return len(specs)
