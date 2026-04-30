# Legend sets

`LegendSetsAccessor` on `Dhis2Client.legend_sets` — create / read / clone / delete LegendSets that visualizations and maps reference by UID to colour their data.

A DHIS2 `LegendSet` is an ordered list of `Legend` entries, each assigning a colour (`#RRGGBB` hex) + display name to a half-open numeric range `[startValue, endValue)`. At render time DHIS2 buckets each cell by which legend its value falls into and paints it with that legend's colour. Visualizations reference a legend set via `VisualizationSpec(legend_set=<uid>, ...)`; maps via `MapSpec(legend_set=<uid>, ...)` on the thematic layer.

## `LegendSetSpec` + `LegendSpec` — the builder pattern

`LegendSet` and `Legend` are **generated models** — pydantic classes emitted from DHIS2's OpenAPI schema. They carry every field the API can return (roughly 20 on `LegendSet`, 18 on `Legend`) including DHIS2-maintained bookkeeping (`created`, `lastUpdated`, `href`, `access`, `createdBy`, `favorites`, `translations`). When authoring a new legend set, you only care about a handful of those: the name, optional code, the ordered legends, and per-legend `(startValue, endValue, color, name)`. Populating the full model by hand for each new set is tedious and error-prone.

`LegendSetSpec` and `LegendSpec` are the **authoring shapes** — small frozen pydantic models whose fields are the tiny subset the caller actually supplies:

| Spec field | Generated equivalent | Notes |
| --- | --- | --- |
| `LegendSetSpec.uid` | `LegendSet.id` | Optional; `build()` auto-generates an 11-char UID if omitted. |
| `LegendSetSpec.name` | `LegendSet.name` | Required. |
| `LegendSetSpec.code` | `LegendSet.code` | Optional business code. |
| `LegendSetSpec.legends` | `LegendSet.legends[]` | Ordered list of `LegendSpec`s — one per colour range. |
| `LegendSpec.start` | `Legend.startValue` | Inclusive range start. Must be `< end`. |
| `LegendSpec.end` | `Legend.endValue` | Exclusive range end. |
| `LegendSpec.color` | `Legend.color` | Hex `#RRGGBB` or `#RRGGBBAA`. |
| `LegendSpec.name` | `Legend.name` | Optional; auto-named from the numeric range when omitted. |

`LegendSetSpec.build()` materialises the spec into the full typed `LegendSet` with every child `Legend` inlined under `legends[]` (DHIS2's metadata importer requires full objects, not sibling references — see the "Why POST through `/api/metadata`" note below). The builder also generates stable per-legend UIDs, validates that `end > start`, and sets sensible defaults on the `Legend` fields the spec didn't specify.

This is the same pattern the workspace uses for every non-trivial authoring flow:

| Spec | Generated model | Builder method |
| --- | --- | --- |
| `VisualizationSpec` | `Visualization` | `VisualizationsAccessor.create_from_spec` |
| `MapSpec` + `MapLayerSpec` | `Map` + `MapView` | `MapsAccessor.create_from_spec` |
| `LegendSetSpec` + `LegendSpec` | `LegendSet` + `Legend` | `LegendSetsAccessor.create_from_spec` |
| `OptionSpec` | `Option` | `OptionSetsAccessor.sync` |

Rule of thumb: a `*Spec` exists only where the accessor needs to transform caller intent into a wire shape the generated model can't represent directly. Three concrete reasons drive every spec in the workspace:

- A typed enum on the spec fans out into many boolean flags on the wire — `VisualizationSpec.relative_periods: frozenset[RelativePeriod]` materialises into 45 individual booleans on `Visualization.relativePeriods`.
- One field selects the population rule for others — `VisualizationSpec.viz_type` picks chart-type-aware `rows` / `columns` / `filters` defaults; `MapLayerSpec.layer_kind` decides whether dimension selectors are populated at all.
- A parent's children need server-correct UIDs / defaults the caller shouldn't have to invent — `LegendSetSpec.build()` mints per-`Legend` UIDs so re-runs are well-formed.

Every other write accessor — `organisation_units`, `data_elements`, `indicators`, `categories`, `category_options`, `category_combos`, `programs`, `program_stages`, `tracked_entity_attributes`, `validation_rules`, `predictors`, `data_sets`, and the rest — ships *without* a spec. The generated model already mirrors what DHIS2 accepts on POST, so the accessor takes plain keyword args and posts them. Reach for a spec only when the accessor needs to do transformation work like the three above; reach for kwargs in every other case.

## Why POST through `/api/metadata`

A direct `PUT /api/legendSets/{uid}` with a sibling `legends` collection is rejected by DHIS2's importer — the importer doesn't cross-link `legends` references back into the parent `LegendSet`, so every child needs to be inlined under `legendSets[*].legends[]` as a full object. `LegendSetSpec.build()` handles this by generating a `LegendSet` with inline `Legend` children already dumped; `LegendSetsAccessor.create_from_spec` POSTs the whole object atomically via `/api/metadata?importStrategy=CREATE_AND_UPDATE&atomicMode=OBJECT`.

## Typed builder

```python
from dhis2_client import LegendSpec, LegendSetSpec

spec = LegendSetSpec(
    name="Dose coverage",
    code="DOSE_COVERAGE",
    legends=[
        LegendSpec(start=0, end=50, color="#d73027", name="Low"),
        LegendSpec(start=50, end=80, color="#fdae61", name="Medium"),
        LegendSpec(start=80, end=120, color="#1a9850", name="High"),
    ],
)
async with Dhis2Client(...) as client:
    legend_set = await client.legend_sets.create_from_spec(spec)
```

`LegendSpec.end` must be strictly greater than `start` — the builder rejects inverted / zero-width ranges. Each child `Legend` gets a fresh UID on `build()` so the spec is idempotent across re-runs only when the caller supplies a fixed `uid` on the spec itself; otherwise each run produces a new set.

## Attach to a visualization

```python
from dhis2_client import VisualizationSpec
from dhis2_client.generated.v42.enums import VisualizationType

viz_spec = VisualizationSpec(
    name="BCG doses 2024 monthly",
    viz_type=VisualizationType.COLUMN,
    data_elements=["s46m5MS0hxu"],
    periods=[f"2024{m:02d}" for m in range(1, 13)],
    organisation_units=["ImspTQPwCqd"],
    legend_set=legend_set.id,  # <- threshold colouring on render
)
```

The workspace seed (`infra/scripts/seed/workspace_fixtures.py`) ships `LsDoseBand1` — four colour ranges tuned to 2024 monthly dose-count totals (red < 2k, amber 2–5k, yellow 5–10k, green 10k+) — and attaches it to `uwtuVAnbt6E` (Measles monthly) and `D3oOqWAM0az` (Penta-1 monthly) on the Immunization dashboard.

::: dhis2_client.legend_sets
