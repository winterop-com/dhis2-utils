"""Visualization authoring helpers — `Dhis2Client.visualizations`.

DHIS2 `Visualization` is one of the richest schemas on the instance —
every combination of chart type, axis placement, legend, periods, and
data dimensions is one model. Most day-to-day authoring only touches a
small subset: the chart type, one or more data elements, a period
selection, an org-unit set, and which of those three dimensions lands on
the category axis / series / filter.

This module layers three things over the generated
`client.resources.visualizations` CRUD accessor:

- `VisualizationSpec` — a typed builder covering the common authoring
  surface with sensible defaults per chart type. Produces a full
  `Visualization` ready to POST via `/api/metadata`.
- `VisualizationsAccessor` — `Dhis2Client.visualizations` — provides
  `list / get / create_from_spec / clone / delete`, all round-tripping
  typed models.
- `DashboardSlot` + helpers used by `Dhis2Client.dashboards.add_item`
  (see `dashboards.py`).

## Dimensional placement cheat-sheet

DHIS2 visualizations have three dimensions — `dx` (data), `pe` (period),
`ou` (org unit) — distributed across three slots:

- `rows` (category axis on charts; left side of a pivot)
- `columns` (series on charts; top of a pivot)
- `filters` (narrow to single value(s); invisible on the canvas)

`VisualizationSpec._resolve_placement()` picks sensible defaults per
`VisualizationType`:

- **LINE / COLUMN / STACKED_COLUMN / BAR / STACKED_BAR / AREA / RADAR /
  PIE**: `rows=[pe]`, `columns=[ou]`, `filters=[dx]` — time runs along
  the x-axis, one series per org unit, single data element filter.
- **PIVOT_TABLE**: `rows=[ou]`, `columns=[pe]`, `filters=[dx]` — the
  shape DHIS2 UIs ship as the default pivot layout.
- **SINGLE_VALUE**: `rows=[]`, `columns=[dx]`, `filters=[pe, ou]` — grid
  collapses to one cell so the KPI tile renders a single number.

Callers override any of those via `category_dimension` /
`series_dimension` / `filter_dimension` when the data shape needs a
different layout (e.g. one line per data element).

## Why POST through `/api/metadata`

A direct `PUT /api/visualizations/{uid}` with `rowDimensions` /
`columnDimensions` / `filterDimensions` set does *not* populate the
derived `rows` / `columns` / `filters` collections — DHIS2 silently
accepts the PUT and stores empty axes, which the dashboard app
surfaces as "A end date was not specified" or an empty grid. Routing
through `/api/metadata?importStrategy=CREATE_AND_UPDATE` runs the
same importer the UI does and expands the dimension selectors into
the axes DHIS2 reads at render time. The accessor always takes that
path; don't bypass it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, model_validator

from dhis2w_client.generated.v43.enums import VisualizationType
from dhis2w_client.generated.v43.oas import RelativePeriods
from dhis2w_client.generated.v43.schemas import Visualization
from dhis2w_client.v43.envelopes import WebMessageResponse
from dhis2w_client.v43.periods import RelativePeriod
from dhis2w_client.v43.uids import generate_uid

if TYPE_CHECKING:
    from dhis2w_client.v43.client import Dhis2Client


_VIZ_FIELDS: str = (
    "id,name,description,type,created,lastUpdated,"
    "columnDimensions,rowDimensions,filterDimensions,"
    "dataDimensionItems[dataDimensionItemType,dataElement[id,name],"
    "indicator[id,name],programIndicator[id,name]],"
    "rawPeriods,organisationUnits[id,name],"
    "columns[id,items[id,dimensionItemType]],"
    "rows[id,items[id,dimensionItemType]],"
    "filters[id,items[id,dimensionItemType]]"
)

_CHART_TYPES: frozenset[VisualizationType] = frozenset(
    {
        VisualizationType.LINE,
        VisualizationType.COLUMN,
        VisualizationType.STACKED_COLUMN,
        VisualizationType.BAR,
        VisualizationType.STACKED_BAR,
        VisualizationType.AREA,
        VisualizationType.STACKED_AREA,
        VisualizationType.PIE,
        VisualizationType.RADAR,
        VisualizationType.GAUGE,
        VisualizationType.YEAR_OVER_YEAR_LINE,
        VisualizationType.YEAR_OVER_YEAR_COLUMN,
        VisualizationType.SCATTER,
        VisualizationType.BUBBLE,
    },
)


DimensionAxis = Literal["dx", "pe", "ou"]


class VisualizationSpec(BaseModel):
    """Typed builder for the common visualization shapes DHIS2 exposes.

    Captures the high-value authoring surface — chart type, data
    elements, periods, org units, and dimensional placement — and
    produces a full `Visualization` via `to_visualization()`. Use
    `client.visualizations.create_from_spec(spec)` to round-trip
    through `/api/metadata` (the only path that fully populates
    DHIS2's derived axes — see the module docstring).
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=230)
    viz_type: VisualizationType = VisualizationType.COLUMN
    data_elements: list[str] = Field(default_factory=list)
    indicators: list[str] = Field(default_factory=list)
    periods: list[str] = Field(default_factory=list)
    relative_periods: frozenset[RelativePeriod] = Field(default_factory=frozenset)
    organisation_units: list[str] = Field(..., min_length=1)
    description: str | None = None
    uid: str | None = None
    category_dimension: DimensionAxis | None = None
    series_dimension: DimensionAxis | None = None
    filter_dimension: DimensionAxis | None = None
    legend_set: str | None = None

    @model_validator(mode="after")
    def _require_period_selection(self) -> VisualizationSpec:
        """Enforce that at least one period slot is populated.

        A `Visualization` without any period dimension has nothing on
        the x-axis for charts / no row-or-column anchor for pivots, and
        DHIS2 resolves it to "No data available" at render time. Failing
        fast at spec construction catches the mistake before the POST.
        """
        if not self.periods and not self.relative_periods:
            raise ValueError("VisualizationSpec requires either `periods` or `relative_periods` (or both)")
        return self

    @model_validator(mode="after")
    def _require_data_dimension(self) -> VisualizationSpec:
        """Enforce that at least one data-dimension item is selected.

        DHIS2 needs at least one `DATA_ELEMENT` / `INDICATOR` /
        `PROGRAM_INDICATOR` entry on the `dx` axis — a viz with zero
        `dataDimensionItems` has nothing to plot and the importer
        rejects it opaquely. Catch it at spec construction.
        """
        if not self.data_elements and not self.indicators:
            raise ValueError("VisualizationSpec requires at least one `data_elements` or `indicators` entry")
        return self

    def to_visualization(self) -> Visualization:
        """Materialise the typed `Visualization` DHIS2's metadata importer accepts."""
        rows, columns, filters = self._resolve_placement()
        data_dimension_items: list[dict[str, Any]] = [
            {"dataDimensionItemType": "DATA_ELEMENT", "dataElement": {"id": uid}} for uid in self.data_elements
        ]
        data_dimension_items.extend(
            {"dataDimensionItemType": "INDICATOR", "indicator": {"id": uid}} for uid in self.indicators
        )
        payload: dict[str, Any] = {
            "id": self.uid or generate_uid(),
            "name": self.name,
            "description": self.description,
            "type": self.viz_type.value,
            "dataDimensionItems": data_dimension_items,
            "rawPeriods": list(self.periods),
            "organisationUnits": [{"id": ou} for ou in self.organisation_units],
            "rowDimensions": rows,
            "columnDimensions": columns,
            "filterDimensions": filters,
        }
        if self.relative_periods:
            # Serialize through the typed `RelativePeriods` model so the boolean
            # field-name discipline is enforced, then dump to a plain dict —
            # the `schemas/Visualization` model stores the block via
            # `extra="allow"` rather than a first-class field, so only dicts
            # round-trip cleanly through `model_validate`.
            relative_periods_model = RelativePeriods(**{p.value: True for p in self.relative_periods})
            payload["relativePeriods"] = relative_periods_model.model_dump(exclude_none=True)
        if self.legend_set is not None:
            # Attach a LegendSet so DHIS2 bands values into the legend's
            # ranges (coverage <50% red, >=90% green). `strategy=FIXED`
            # applies the single legend to every data item; `style=FILL`
            # colours the bar/cell (not just the text); `showKey=true`
            # renders the legend key on the chart.
            payload["legend"] = {
                "set": {"id": self.legend_set},
                "strategy": "FIXED",
                "style": "FILL",
                "showKey": True,
            }
        return Visualization.model_validate(payload)

    def _resolve_placement(self) -> tuple[list[str], list[str], list[str]]:
        """Default dimension placement per `VisualizationType`.

        Returns `(rowDimensions, columnDimensions, filterDimensions)`
        as lists of `"dx" | "pe" | "ou"` tokens. Overrides from
        `category_dimension` / `series_dimension` / `filter_dimension`
        take precedence and shift the remaining dimensions to filters.
        """
        if self.viz_type == VisualizationType.SINGLE_VALUE:
            # SV: grid collapses to one cell. `dx` on columns by
            # default, everything else on filters, rows stays empty.
            series = self.series_dimension or "dx"
            remaining: list[str] = [d for d in ("dx", "pe", "ou") if d != series and d != self.category_dimension]
            category: list[str] = [self.category_dimension] if self.category_dimension is not None else []
            return category, [series], remaining
        if self.viz_type == VisualizationType.PIVOT_TABLE:
            rows = self.category_dimension or "ou"
            columns = self.series_dimension or "pe"
            filters = self.filter_dimension or _remaining_axis(rows, columns)
            return [rows], [columns], [filters]
        if self.viz_type in _CHART_TYPES:
            rows = self.category_dimension or "pe"
            columns = self.series_dimension or "ou"
            filters = self.filter_dimension or _remaining_axis(rows, columns)
            return [rows], [columns], [filters]
        # Unknown / future types fall back to the chart convention.
        rows = self.category_dimension or "pe"
        columns = self.series_dimension or "ou"
        filters = self.filter_dimension or _remaining_axis(rows, columns)
        return [rows], [columns], [filters]


class VisualizationsAccessor:
    """`Dhis2Client.visualizations` — workflow helpers over `/api/visualizations`."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        viz_type: VisualizationType | str | None = None,
    ) -> list[Visualization]:
        """List every Visualization, optionally narrowed by type. Sorted by name."""
        filters: list[str] | None = None
        if viz_type is not None:
            value = viz_type.value if isinstance(viz_type, VisualizationType) else viz_type
            filters = [f"type:eq:{value}"]
        return cast(
            list[Visualization],
            await self._client.resources.visualizations.list(
                fields="id,name,description,type,lastUpdated",
                filters=filters,
                order=["name:asc"],
                paging=False,
            ),
        )

    async def get(self, uid: str) -> Visualization:
        """Fetch one Visualization with axes + data dimensions resolved inline."""
        raw = await self._client.get_raw(f"/api/visualizations/{uid}", params={"fields": _VIZ_FIELDS})
        return Visualization.model_validate(raw)

    async def create_from_spec(self, spec: VisualizationSpec) -> Visualization:
        """Build a Visualization from a spec and POST via `/api/metadata`.

        The metadata importer expands `rowDimensions` / `columnDimensions`
        / `filterDimensions` into the derived `rows` / `columns` /
        `filters` collections DHIS2 actually renders from. A direct
        `PUT /api/visualizations/{uid}` skips that expansion and stores
        empty axes — don't take that shortcut.
        """
        viz = spec.to_visualization()
        if viz.id is None:
            raise ValueError("VisualizationSpec did not assign a UID — check to_visualization()")
        body = {"visualizations": [viz.model_dump(by_alias=True, exclude_none=True, mode="json")]}
        raw = await self._client.post_raw(
            "/api/metadata",
            body,
            params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL"},
        )
        WebMessageResponse.model_validate(raw)
        return await self.get(viz.id)

    async def clone(
        self,
        source_uid: str,
        *,
        new_name: str,
        new_uid: str | None = None,
        new_description: str | None = None,
    ) -> Visualization:
        """Duplicate an existing Visualization with a fresh UID + new name.

        Copies the full axes / data dimensions / period / org-unit
        selection so the clone renders identically. Reset any display
        overrides (title / subtitle) by passing `new_description=...`
        explicitly — the source's description carries over otherwise.
        """
        source = await self.get(source_uid)
        target_uid = new_uid or generate_uid()
        payload = source.model_dump(by_alias=True, exclude_none=True, mode="json")
        # Strip server-owned + identity fields so the clone is treated
        # as a fresh create rather than an update of the source.
        for owned in (
            "id",
            "uid",
            "created",
            "lastUpdated",
            "createdBy",
            "lastUpdatedBy",
            "href",
            "access",
            "user",
            "favorites",
            "favorite",
            "subscribers",
            "subscribed",
            "interpretations",
            "displayName",
            "displayDescription",
            "displayFormName",
            "displayShortName",
            "displaySubtitle",
            "displayTitle",
            "translations",
        ):
            payload.pop(owned, None)
        payload["id"] = target_uid
        payload["name"] = new_name
        if new_description is not None:
            payload["description"] = new_description
        raw = await self._client.post_raw(
            "/api/metadata",
            {"visualizations": [payload]},
            params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL"},
        )
        WebMessageResponse.model_validate(raw)
        return await self.get(target_uid)

    async def delete(self, uid: str) -> None:
        """DELETE a Visualization by UID."""
        await self._client.resources.visualizations.delete(uid)


def _remaining_axis(used_a: str, used_b: str) -> str:
    """Return the one dimension not yet used across rows + columns."""
    remaining = {"dx", "pe", "ou"} - {used_a, used_b}
    if len(remaining) != 1:
        raise ValueError(f"invalid placement: rows={used_a!r} columns={used_b!r}")
    return remaining.pop()


__all__ = [
    "DimensionAxis",
    "VisualizationSpec",
    "VisualizationsAccessor",
]
