# Metadata plugin

`dhis2-core/plugins/metadata/` wraps the 119 generated CRUD resources in a uniform CLI + MCP surface. It's a thin layer — the real work is in the generated `client.resources.<name>` accessors (see [Metadata CRUD](metadata-crud.md) for the underlying resources, [Plugin runtime](plugins.md) for the mounting pattern).

## What it exposes

Three operations, available as both CLI subcommands and MCP tools:

| Operation | CLI | MCP tool |
| --- | --- | --- |
| List available resource types | `dhis2 metadata type list` | `metadata_type_list` |
| List instances of one type | `dhis2 metadata list <resource>` | `metadata_list` |
| Fetch one by UID | `dhis2 metadata get <resource> <uid>` | `metadata_get` |

The `<resource>` argument is DHIS2's camelCase plural — `dataElements`, `indicators`, `organisationUnits`, `dashboards`, `dataSets`, …. The plugin maps it to the Resources attribute (`data_elements`, etc.) via a tiny camel-to-snake helper.

## CLI examples

```bash
# Discover what this instance exposes
dhis2 metadata type list
# → data_elements, indicators, organisation_units, ... (119 types)

# List with a rich table (default)
dhis2 metadata list dataElements --fields id,name --limit 10
# ┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ id          ┃ name                       ┃
# ┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │ fbfJHSPpUQD │ ANC 1st visit              │
# │ cYeuwXTCPkU │ ANC 2nd visit              │
# └─────────────┴────────────────────────────┘

# Or as JSON for pipelines
dhis2 metadata list indicators --fields id,displayName --filter 'name:like:Malaria' --json

# Single get
dhis2 metadata get dataElements fbfJHSPpUQD --fields id,name,aggregationType,valueType
```

## MCP example

An agent calls:

```python
await mcp.call_tool("metadata_type_list", {})
# → ["data_elements", "indicators", "organisation_units", ...]

await mcp.call_tool("metadata_list", {
    "resource": "dataElements",
    "fields": "id,displayName,aggregationType",
    "filter": "name:like:Malaria",
    "limit": 25,
})
# → [{"id": "abc", "displayName": "Malaria cases"}, ...]

await mcp.call_tool("metadata_get", {
    "resource": "dataElements",
    "uid": "fbfJHSPpUQD",
})
# → { full typed model as dict }
```

## Why a dict return (not the pydantic model)

FastMCP can return pydantic models, but MCP agents expect JSON-serializable output. Returning `list[dict[str, Any]]` gives agents reliable consumption without introducing a tooling dependency on pydantic shapes. `_dump()` in the service uses `model_dump(by_alias=True, exclude_none=True, mode="json")` so datetimes, UUIDs, and nested refs serialise cleanly.

## Error handling

- Requesting an unknown resource raises `UnknownResourceError` with a helpful message suggesting `list_resource_types`. Both CLI and MCP surface this as an actionable error the agent/user can recover from.
- Other server-side errors (403, 409, 500) propagate as `Dhis2ApiError` — the FastMCP protocol wraps them as tool-error results with the DHIS2 message body attached.

## Limits

The `limit` param slices client-side after the list response returns. True server-side pagination (`paging=true` + `page`) isn't threaded through yet — `list_raw` on the generated resources supports it, but the plugin's typed `list` uses single-shot `paging=false`. Most uses (top-N browsing, filtered lookups) are fine with the client-side truncation; when we need streaming, the plugin gains a `list_paged` that iterates server pages.
