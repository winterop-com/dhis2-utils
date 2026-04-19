# Analytics plugin

`dhis2-core/plugins/analytics/` wraps DHIS2's analytics API at `/api/analytics` and the analytics-table management endpoint at `/api/resourceTables/analytics`. The analytics engine is DHIS2's aggregation pipeline — pre-computed tables behind every dashboard, pivot table, and data query.

## What it exposes

| Operation | CLI | MCP tool |
| --- | --- | --- |
| Aggregated query | `dhis2 analytics query` | `analytics_query` |
| Raw (pre-aggregation) query | `dhis2 analytics query --shape raw` | `analytics_query (shape=raw)` |
| DataValueSet-shaped output | `dhis2 analytics query --shape dvs` | `analytics_query (shape=dvs)` |
| Trigger analytics rebuild | `dhis2 analytics refresh` | `analytics_refresh` |

## Dimensions and filters

Every analytics query is built from **dimensions** (rows/columns you want to see) and **filters** (rows/columns you want to constrain but not display).

Each dimension is a string `<type>:<UID[;UID...]>` or `<type>:<keyword>`:

| Type prefix | What it is | Example |
| --- | --- | --- |
| `dx` | Data — data elements, indicators, data sets, event data | `dx:fbfJHSPpUQD;cYeuwXTCPkU` |
| `pe` | Periods | `pe:LAST_12_MONTHS` or `pe:202401;202402` |
| `ou` | Organisation units | `ou:ImspTQPwCqd` or `ou:LEVEL-2;OU_GROUP-ABC` |
| `co` | Category option combos | `co:KsP9obVY8jF` |
| `ao` | Attribute option combos | `ao:...` |

Period keywords DHIS2 understands include `LAST_12_MONTHS`, `LAST_6_MONTHS`, `THIS_MONTH`, `LAST_YEAR`, `THIS_QUARTER`, `LAST_4_QUARTERS`, `LAST_5_YEARS`, etc.

## CLI examples

```bash
# Simple aggregated query: one data element over the last 12 months at a specific org unit
dhis2 analytics query \
  --dim dx:fbfJHSPpUQD \
  --dim pe:LAST_12_MONTHS \
  --dim ou:ImspTQPwCqd \
  --skip-meta

# Multiple data elements + a filter
dhis2 analytics query \
  --dim 'dx:fbfJHSPpUQD;cYeuwXTCPkU' \
  --dim pe:LAST_12_MONTHS \
  --dim ou:ImspTQPwCqd \
  --filter co:KsP9obVY8jF \
  --agg SUM \
  --output-id-scheme NAME

# Raw data variant (no server-side aggregation)
dhis2 analytics query --shape raw \
  --dim dx:fbfJHSPpUQD \
  --dim pe:LAST_3_MONTHS \
  --dim ou:ImspTQPwCqd

# DataValueSet shape (for pipelines that want dataValues[] output)
dhis2 analytics query --shape dvs \
  --dim dx:fbfJHSPpUQD \
  --dim pe:LAST_12_MONTHS \
  --dim ou:ImspTQPwCqd

# Trigger a rebuild of the analytics tables (async; returns a task reference).
dhis2 analytics refresh --last-years 2

# Same, but stream notifications until the table rebuild reports completed=true.
dhis2 analytics refresh --last-years 2 --watch --interval 1 --timeout 300

# Event analytics — line-listed events in a program.
dhis2 analytics events query <PROG_UID> \
  --dim pe:LAST_12_MONTHS \
  --dim ou:<OU_UID> \
  --stage <STAGE_UID>

# Event analytics — aggregated counts grouped by the supplied dimensions.
dhis2 analytics events query <PROG_UID> --mode aggregate \
  --dim dx:<DATA_ELEMENT_UID> --dim pe:LAST_12_MONTHS --dim ou:<OU_UID>

# Enrollment analytics — line-listed enrollments.
dhis2 analytics enrollments query <PROG_UID> \
  --dim pe:LAST_12_MONTHS --start-date 2026-01-01 --end-date 2026-06-30
```

## MCP examples

```python
# Aggregated query
await mcp.call_tool("analytics_query", {
    "dimensions": [
        "dx:fbfJHSPpUQD;cYeuwXTCPkU",
        "pe:LAST_12_MONTHS",
        "ou:ImspTQPwCqd",
    ],
    "aggregation_type": "SUM",
    "output_id_scheme": "NAME",
    "include_num_den": True,
})

# Raw
await mcp.call_tool("analytics_query (shape=raw)", {
    "dimensions": ["dx:fbfJHSPpUQD", "pe:LAST_3_MONTHS", "ou:ImspTQPwCqd"],
})

# Trigger rebuild
await mcp.call_tool("analytics_refresh", {"last_years": 2})
```

## Response shape

```json
{
  "headers": [
    {"name": "dx", "column": "Data", "valueType": "TEXT", ...},
    {"name": "pe", "column": "Period", "valueType": "TEXT", ...},
    {"name": "ou", "column": "Organisation unit", "valueType": "TEXT", ...},
    {"name": "value", "column": "Value", "valueType": "NUMBER", ...}
  ],
  "rows": [
    ["fbfJHSPpUQD", "202401", "ImspTQPwCqd", "4852"],
    ["fbfJHSPpUQD", "202402", "ImspTQPwCqd", "4911"],
    ...
  ],
  "metaData": {
    "dimensions": { "dx": [...], "pe": [...], "ou": [...] },
    "items": { "fbfJHSPpUQD": {"name": "ANC 1st visit"}, ... }
  },
  "width": 4,
  "height": N
}
```

`metaData` is the item-name dictionary — use it to translate UIDs to human-readable labels. `skip_meta=True` strips this section for lighter payloads when the caller already knows the UIDs.

## Refresh is asynchronous

`analytics_refresh` returns a DHIS2 task reference:

```json
{"response": {"id": "KjN4PQxQDkO", "jobType": "ANALYTICS_TABLE"}}
```

Poll `/api/system/tasks/ANALYTICS_TABLE/{taskId}` to watch progress. A typical refresh on a small instance takes 1–5 minutes; production instances can be 30+ minutes. The analytics tables need regeneration whenever data values change beyond the last-refresh window.

## Output ID schemes

By default, UIDs stay as UIDs in responses. Set `output_id_scheme` to:

- `UID` — default
- `NAME` — replace UIDs with display names (human-readable)
- `CODE` — use the object's code field if set
- `ID` — numeric database ID (not recommended; changes across instances)

## Outlier detection

`/api/analytics/outlierDetection` flags anomalous data values against the
standard-deviation profile of their series. Three algorithms supported
upstream: `Z_SCORE` (default), `MOD_Z_SCORE` (median-based, robust to
existing outliers), and `MIN_MAX` (hard-bound cutoffs).

```bash
# Outliers across one data set + the Oslo org unit for the last 12 months:
dhis2 analytics outlier-detection \
    --data-set NORMonthDS1 \
    --org-unit NOROsloProv \
    --period LAST_12_MONTHS \
    --algorithm Z_SCORE --threshold 2.0 --max-results 10

# Or a narrow set of data elements over an explicit date range:
dhis2 analytics outlier-detection \
    --data-element DEancVisit1 --data-element DEdelFacilt \
    --org-unit NORNordland \
    --start-date 2025-01-01 --end-date 2025-12-31 \
    --algorithm MOD_Z_SCORE
```

Returns a typed `OutlierDetectionResponse` (OAS-generated):
`.metadata` has the effective algorithm + threshold + count; `.outlierValues`
is a list of `OutlierValue` entries with `de`, `deName`, `pe`, `ou`, `ouName`,
`value`, `mean`, `stdDev`, `absDev`, and `zScore`.

## Tracked entity analytics

`/api/analytics/trackedEntities/query/{TET_UID}` line-lists tracked entities
of a given type, with the same dimension/filter grammar as event/enrollment
analytics.

```bash
dhis2 analytics tracked-entities query FsgEX4d3Fc5 \
    --dimension ou:NORNorway01 --ou-mode DESCENDANTS \
    --program eke95YJi9VS \
    --page-size 50 --asc created
```

Returns `AnalyticsResponse` with the familiar headers/rows/metaData envelope.
Useful for exporting a TET slice to external BI or building a registry view;
the `--asc` / `--desc` flags sort on any response column.

## Not yet exposed

- **Measure criteria with multiple operators** — `--measure-criteria EQ:42:GT:100` etc.
- **Response format overrides** — `.csv`, `.xml`, `.xlsx` variants. Current output is always JSON.

The plugin's `service.py` is small; extensions land as new service functions + one CLI command + one MCP tool per.
