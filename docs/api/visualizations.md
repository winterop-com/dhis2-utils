# Visualizations + dashboards

`VisualizationsAccessor` on `Dhis2Client.visualizations` + `DashboardsAccessor` on `Dhis2Client.dashboards` cover the authoring surface over `/api/visualizations` and `/api/dashboards`. `VisualizationSpec` is a typed builder that turns chart type + data elements + periods + org units + dimensional placement into a full `Visualization` that DHIS2's metadata importer accepts. `DashboardSlot` models the 60-unit-wide grid placement used by `DashboardsAccessor.add_item`.

Generic CRUD remains on `client.resources.visualizations` and `client.resources.dashboards` (the generated accessors). The helpers here layer the *workflow* pieces — spec-driven creation, clone, add/remove dashboard items — that the bare generated API forces callers to hand-roll.

## `VisualizationSpec` — builder over the generated `Visualization`

`Visualization` is the **generated model** — emitted from DHIS2's OpenAPI schema with ~70 fields covering every knob the Data Visualizer app writes (plus DHIS2 bookkeeping: `created`, `lastUpdated`, `href`, `access`, `favorites`, `translations`). Authoring a chart by populating that model directly is tedious.

`VisualizationSpec` is the **authoring shape** — a frozen pydantic model whose fields are the tiny subset the caller actually supplies: `name`, `viz_type`, `data_elements` / `indicators` / `program_indicators`, `periods`, `organisation_units`, optional dimensional placement overrides, optional `legend_set`. `VisualizationsAccessor.create_from_spec` calls `.build()` internally to materialise the spec into the full typed `Visualization` that DHIS2's metadata importer accepts.

The spec exists because the wire shape needs transformation the generated `Visualization` doesn't carry on its own — chart-type-aware `rows` / `columns` / `filters` defaults driven off `viz_type` (see [Dimensional placement](#dimensional-placement) below), and `RelativePeriod` enum fan-out into the 45 individual boolean fields DHIS2 exposes on `Visualization.relativePeriods`. Plain keyword args on `accessor.create(...)` would push both jobs onto every caller. Same pattern as `MapSpec` / `MapLayerSpec` / `LegendSetSpec` / `LegendSpec` / `OptionSpec` — see the [Legend sets doc](legend-sets.md#legendsetspec-legendspec-the-builder-pattern) for the full spec-vs-generated-model cross-reference table and the rule for when reaching for a spec is the right call.

## Dimensional placement

Every Visualization distributes the three DHIS2 analytics dimensions — `dx` (data), `pe` (period), `ou` (org unit) — across three slots:

- `rows` — category axis on charts, left side of pivot tables
- `columns` — series (legend colours) on charts, top of pivot tables
- `filters` — narrows to specific items without occupying the canvas

`VisualizationSpec._resolve_placement()` picks sensible defaults per `VisualizationType`:

| Type family | rows | columns | filters |
| --- | --- | --- | --- |
| `LINE` / `COLUMN` / `STACKED_COLUMN` / `BAR` / `STACKED_BAR` / `AREA` / `RADAR` / `PIE` | `pe` | `ou` | `dx` |
| `PIVOT_TABLE` | `ou` | `pe` | `dx` |
| `SINGLE_VALUE` | *(empty)* | `dx` | `pe, ou` |

Override any slot explicitly via `category_dimension` / `series_dimension` / `filter_dimension` when the data shape needs a different layout.

## Why everything goes through `/api/metadata`

A direct `PUT /api/visualizations/{uid}` with `rowDimensions` / `columnDimensions` / `filterDimensions` set does **not** populate the derived `rows` / `columns` / `filters` collections that DHIS2 renders from. DHIS2 silently accepts the PUT, stores empty axes, and the dashboard app surfaces "A end date was not specified" or an empty grid. Routing through `POST /api/metadata?importStrategy=CREATE_AND_UPDATE` runs the same importer the UI does and expands the dimension selectors into the axes DHIS2 reads at render time. `VisualizationsAccessor.create_from_spec` and `DashboardsAccessor.add_item` both take that path; don't bypass them.

## Related

- [Analytics](analytics.md) — `client.analytics.aggregate(...)` hits the same dimension model (`dx`, `pe`, `ou`) that powers visualizations. Every saved Visualization is essentially a persisted analytics query with a chart type + axis placement attached.
- [Client tutorial — visualizations guide](../guides/visualizations.md) — end-to-end walkthrough covering spec-driven authoring, clone, dashboard composition, and the screenshot path.

::: dhis2w_client.visualizations

::: dhis2w_client.dashboards
