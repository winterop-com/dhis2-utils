"""Programmatic visualization build for the Sierra Leone immunization seed.

The play42 snapshot at `infra/fixtures/play/metadata.json` ships 23 hand-crafted
visualizations across the 3 dashboards (`Immunization` TAMlzYkstb7,
`Immunization data` L1BtjXgpUpd, `Measles` KQVXh5tlzW2). Half of them reference
indicators we don't transitively import, and most use rolling windows that
blank out against our 1-year (2024) aggregate data seed.

Rather than import them as JSON and ship broken tiles, this module
reconstructs each viz via `Dhis2Client.visualizations.create_from_spec(...)`:

- Sierra Leone DE + Indicator UIDs for every `dataDimensionItems` entry.
- Explicit monthly periods `202401..202412` for time-series charts, yearly
  `["2024"]` for single-value tiles, so the charts render real monthly
  detail against the only year we have data for. Two specs keep
  `RelativePeriod.LAST_5_YEARS` to exercise the rolling-window path of the
  builder API (these will pick up more data automatically if the fixture's
  period range widens later).
- The original UID is carried on each spec so every dashboard item in the
  bundle resolves to the rebuilt viz without touching `dashboardItems`.

Called from `seed_play` after the core metadata pass (which imports DEs,
indicators, maps, etc. but skips `visualizations`) and before the dashboard
pass, so the dashboards land in the same import but resolve their items
against freshly-created vizes.

Known follow-up: to exercise the rolling-window path (`LAST_12_MONTHS` /
`LAST_4_QUARTERS` etc.) against the live stack, extend
`infra/scripts/pull_play_fixtures.py` to duplicate + jitter the 2024
aggregate values into 2023/2025 so rolling windows have data to hit.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from dhis2_client import RelativePeriod, VisualizationSpec
from dhis2_client.generated.v42.enums import VisualizationType

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


# Sierra Leone root — every viz pins to the country root (admin is already
# attached to it by the time seed_play reaches this pass).
_SL_ROOT = "ImspTQPwCqd"

# Core immunization data elements pulled from the play Child Health dataset.
# One canonical UID per dose stage so callers can mix-and-match by intent.
_DE_BCG = "s46m5MS0hxu"
_DE_MEASLES = "YtbsuPPo010"
_DE_PENTA1 = "fClA2Erf6IO"
_DE_PENTA2 = "I78gJm4KBo7"
_DE_PENTA3 = "n6aMJNLdvep"
_DE_FIC = "UOlfIjgN8X6"

# The three indicators we DO transitively pull — Stock-PHU variants.
# Used on the handful of vizes where a stock view is the natural read.
_IND_BCG_STOCK = "OEWO2PpiUKx"
_IND_OPV_STOCK = "bASXd9ukRGD"
_IND_MEASLES_STOCK = "loEBZlcsTlx"

# Immunization Coverage legend set — <50% red, 50-89% amber, 90%+ green.
# Transitively pulled from the play snapshot. Bands dose counts on
# coverage-style charts so the colour carries the clinical reading.
_LEGEND_IMMUNIZATION_COVERAGE = "BtxOoQuLyg1"

# Fixed monthly + yearly periods covering the seed's 2024 aggregate data.
_MONTHS_2024: list[str] = [f"2024{m:02d}" for m in range(1, 13)]
_YEAR_2024: list[str] = ["2024"]


def _immunization_specs() -> list[VisualizationSpec]:
    """Specs for the 12 items on the Immunization dashboard."""
    return [
        VisualizationSpec(
            uid="Qyuliufvfjl",
            name="Immunization: BCG, measles, FIC 2024 monthly (stacked)",
            viz_type=VisualizationType.STACKED_COLUMN,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="tZCI4NSC8dc",
            name="Immunization: Fully immunized by month 2024 (stacked)",
            viz_type=VisualizationType.STACKED_COLUMN,
            data_elements=[_DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
            category_dimension="pe",
            series_dimension="ou",
            legend_set=_LEGEND_IMMUNIZATION_COVERAGE,
        ),
        VisualizationSpec(
            uid="R9A0rvAydpn",
            name="Immunization: BCG, Measles, Penta doses comparison 2024",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_PENTA1, _DE_PENTA2, _DE_PENTA3],
            periods=_YEAR_2024,
            organisation_units=[_SL_ROOT],
            category_dimension="dx",
            series_dimension="pe",
        ),
        VisualizationSpec(
            uid="uwtuVAnbt6E",
            name="Immunization: Measles doses 2024 monthly",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_MEASLES],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
            category_dimension="pe",
            series_dimension="ou",
        ),
        VisualizationSpec(
            uid="pRBQ77mhEJ8",
            name="Immunization: Essential vaccines 2024 monthly",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_PENTA1, _DE_PENTA3, _DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="KmJwftqlU86",
            name="Immunization: Doses by type 2024 monthly",
            viz_type=VisualizationType.PIVOT_TABLE,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_PENTA1, _DE_PENTA2, _DE_PENTA3, _DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
            legend_set=_LEGEND_IMMUNIZATION_COVERAGE,
        ),
        VisualizationSpec(
            uid="D3oOqWAM0az",
            name="Immunization: Penta 1 doses 2024 monthly",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_PENTA1],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
            category_dimension="pe",
            series_dimension="ou",
        ),
        VisualizationSpec(
            uid="DNRhUsVbTgT",
            name="Immunization: Penta 3 doses 2024 total",
            viz_type=VisualizationType.SINGLE_VALUE,
            data_elements=[_DE_PENTA3],
            periods=_YEAR_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="LRFDsb8jcG0",
            name="Immunization: Doses administered 2024 monthly",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_PENTA1, _DE_PENTA2, _DE_PENTA3, _DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="XDjerozqh69",
            name="Immunization: Measles doses 2024 monthly (repeat)",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_MEASLES],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
            category_dimension="pe",
            series_dimension="ou",
        ),
        VisualizationSpec(
            uid="jj2y3G88Dg7",
            name="Immunization: Fully Immunized 2024 monthly",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="m0Fv9zt5E79",
            name="Immunization: BCG, Measles, FIC doses 2024",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_FIC],
            indicators=[_IND_BCG_STOCK, _IND_MEASLES_STOCK, _IND_OPV_STOCK],
            periods=_YEAR_2024,
            organisation_units=[_SL_ROOT],
            category_dimension="dx",
            series_dimension="pe",
        ),
    ]


def _immunization_data_specs() -> list[VisualizationSpec]:
    """Specs for the data-focused tiles on the Immunization data dashboard."""
    return [
        # Line chart uses `LAST_5_YEARS` to demonstrate the relative-period
        # builder path against a yearly aggregation — renders one node on
        # the 2024 mark against our current data, but will naturally extend
        # if the aggregate seed ever covers more years.
        VisualizationSpec(
            uid="R3N0O5KywZe",
            name="Immunization: FIC trend (rolling 5 years)",
            viz_type=VisualizationType.LINE,
            data_elements=[_DE_FIC],
            relative_periods=frozenset({RelativePeriod.LAST_5_YEARS}),
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="cWxQvCytuG5",
            name="Immunization: Stock indicators MCHP 2024",
            viz_type=VisualizationType.PIVOT_TABLE,
            indicators=[_IND_BCG_STOCK, _IND_OPV_STOCK, _IND_MEASLES_STOCK],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
            category_dimension="dx",
            series_dimension="pe",
        ),
        VisualizationSpec(
            uid="FXFCkALrbsC",
            name="Immunization: Data by type 2024 monthly",
            viz_type=VisualizationType.PIVOT_TABLE,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_PENTA1, _DE_PENTA2, _DE_PENTA3, _DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="DrqOYDGA11X",
            name="Immunization: Doses 2024 monthly",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_PENTA1, _DE_PENTA2, _DE_PENTA3, _DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="IDgeKC48UXd",
            name="Immunization: Data by districts 2024 monthly",
            viz_type=VisualizationType.PIVOT_TABLE,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_PENTA1, _DE_PENTA2, _DE_PENTA3, _DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
            legend_set=_LEGEND_IMMUNIZATION_COVERAGE,
        ),
        VisualizationSpec(
            uid="INtKDA1VJC0",
            name="Immunization: All Vaccines 2024 total",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_BCG, _DE_MEASLES, _DE_PENTA1, _DE_PENTA2, _DE_PENTA3, _DE_FIC],
            periods=_YEAR_2024,
            organisation_units=[_SL_ROOT],
        ),
    ]


def _measles_specs() -> list[VisualizationSpec]:
    """Specs for the five rebuilt items on the Measles dashboard."""
    return [
        VisualizationSpec(
            uid="l49Xj5POupZ",
            name="Measles: Coverage and drop-out 2024 monthly",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_MEASLES, _DE_FIC],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="BktEbwJgoxI",
            name="Measles: Follow-up, new, referrals 2024 monthly",
            viz_type=VisualizationType.PIVOT_TABLE,
            data_elements=[_DE_MEASLES, _DE_FIC, _DE_PENTA3],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        # Rolling 5-year window — exercises the relative-period builder
        # path on a pivot table. Yearly aggregation.
        VisualizationSpec(
            uid="WyN08Jo2qpj",
            name="Measles: Follow-up, new, referrals (rolling 5 years)",
            viz_type=VisualizationType.PIVOT_TABLE,
            data_elements=[_DE_MEASLES, _DE_FIC, _DE_PENTA3],
            relative_periods=frozenset({RelativePeriod.LAST_5_YEARS}),
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="GxsiESWvqnt",
            name="Measles: Follow-up, new, referrals 2024 column",
            viz_type=VisualizationType.COLUMN,
            data_elements=[_DE_MEASLES, _DE_FIC, _DE_PENTA3],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
        ),
        VisualizationSpec(
            uid="Ao2PcwdEOeA",
            name="Measles: Stock indicators 2024 monthly",
            viz_type=VisualizationType.PIVOT_TABLE,
            indicators=[_IND_MEASLES_STOCK, _IND_OPV_STOCK],
            periods=_MONTHS_2024,
            organisation_units=[_SL_ROOT],
            category_dimension="dx",
            series_dimension="pe",
        ),
    ]


def all_specs() -> list[VisualizationSpec]:
    """Return every spec the seed creates (23 total across the 3 dashboards)."""
    return [*_immunization_specs(), *_immunization_data_specs(), *_measles_specs()]


async def build_dashboard_visualizations(client: Dhis2Client) -> int:
    """Create every seed visualization via the client's typed builder.

    Each spec is round-tripped through `VisualizationsAccessor.create_from_spec`,
    which POSTs the materialized `Visualization` through `/api/metadata` (the
    only path that fully populates DHIS2's derived `rows` / `columns` /
    `filters` collections — see `dhis2_client.visualizations`).

    Returns the count of vizes created so seed_play can report progress.
    """
    specs = all_specs()
    for spec in specs:
        await client.visualizations.create_from_spec(spec)
    return len(specs)
