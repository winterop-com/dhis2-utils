# Analytics plugin

`dhis2-core/plugins/analytics/` wraps DHIS2's analytics API at `/api/analytics` and the analytics-table management endpoint at `/api/resourceTables/analytics`. The analytics engine is DHIS2's aggregation pipeline — pre-computed tables behind every dashboard, pivot table, and data query.

## What it exposes

| Operation | CLI | MCP tool |
| --- | --- | --- |
| Aggregated query | `dhis2 analytics query` | `query_analytics` |
| Raw (pre-aggregation) query | `dhis2 analytics raw` | `query_analytics_raw` |
| DataValueSet-shaped output | `dhis2 analytics data-value-set` | `query_analytics_data_value_set` |
| Trigger analytics rebuild | `dhis2 analytics refresh` | `refresh_analytics` |

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
dhis2 analytics raw \
  --dim dx:fbfJHSPpUQD \
  --dim pe:LAST_3_MONTHS \
  --dim ou:ImspTQPwCqd

# DataValueSet shape (for pipelines that want dataValues[] output)
dhis2 analytics data-value-set \
  --dim dx:fbfJHSPpUQD \
  --dim pe:LAST_12_MONTHS \
  --dim ou:ImspTQPwCqd

# Trigger a rebuild of the analytics tables
dhis2 analytics refresh --last-years 2
```

## MCP examples

```python
# Aggregated query
await mcp.call_tool("query_analytics", {
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
await mcp.call_tool("query_analytics_raw", {
    "dimensions": ["dx:fbfJHSPpUQD", "pe:LAST_3_MONTHS", "ou:ImspTQPwCqd"],
})

# Trigger rebuild
await mcp.call_tool("refresh_analytics", {"last_years": 2})
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

`refresh_analytics` returns a DHIS2 task reference:

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

## Not yet exposed

- **`/api/analytics/enrollments/query` and `.../events/query`** — specialised tracker analytics. These have a different query shape and get their own plugin when the need arises.
- **Measure criteria with multiple operators** — `--measure-criteria EQ:42:GT:100` etc.
- **Response format overrides** — `.csv`, `.xml`, `.xlsx` variants. Current output is always JSON.

The plugin's `service.py` is small (~100 lines); extensions land as new service functions + one CLI command + one MCP tool per.
