# Metadata plugin

`dhis2-core/plugins/metadata/` wraps the generated CRUD resources in a uniform CLI + MCP surface. It's a thin layer — the real work is in the generated `client.resources.<name>` accessors (see [Metadata CRUD](metadata-crud.md) for the underlying resources, [Plugin runtime](plugins.md) for the mounting pattern).

## What it exposes

Three operations, available as both CLI subcommands and MCP tools:

| Operation | CLI | MCP tool |
| --- | --- | --- |
| List available resource types | `dhis2 metadata type list` | `metadata_type_list` |
| List instances of one type | `dhis2 metadata list <resource>` | `metadata_list` |
| Fetch one by UID | `dhis2 metadata get <resource> <uid>` | `metadata_get` |

The `<resource>` argument is DHIS2's camelCase plural — `dataElements`, `indicators`, `organisationUnits`, `dashboards`, `dataSets`. The plugin maps it to the Resources attribute (`data_elements`, etc.) via a tiny camel-to-snake helper.

## `metadata list` — full flag surface

Every DHIS2 `/api/<resource>` query parameter is exposed:

| Flag | DHIS2 param | Example | Notes |
| --- | --- | --- | --- |
| `--fields` | `fields=` | `--fields ":identifiable"` | See [Field selector](#field-selector). |
| `--filter` | `filter=` | `--filter "name:like:ANC"` | Repeatable. See [Filter syntax](#filter-syntax). |
| `--root-junction` | `rootJunction=` | `--root-junction OR` | Combine multiple `--filter`s. Default `AND`. |
| `--order` | `order=` | `--order "name:asc"` | Repeatable, later clauses tie-break. |
| `--page` | `page=` | `--page 2` | 1-based. Server-side. |
| `--page-size` | `pageSize=` | `--page-size 100` | Default 50 on DHIS2's side. |
| `--all` | `paging=false` + walk | `--all` | Stream every server-side page via `iter_metadata`. |
| `--translate` / `--no-translate` | `translate=` | `--translate` | Return localised `displayName`, etc. |
| `--locale` | `locale=` | `--locale fr` | Pair with `--translate`. |
| `--json` | — | `--json` | Emit JSON instead of a rich table. |

## Filter syntax

DHIS2 filters follow `property:operator:value`:

| Operator | Meaning | Example |
| --- | --- | --- |
| `eq` | equals | `code:eq:DEancVisit1` |
| `!eq` / `ne` | not equal | `code:!eq:REFERENCE` |
| `gt`, `ge`, `lt`, `le` | numeric/date compare | `created:ge:2024-01-01` |
| `like` / `!like` | SQL LIKE (case-sensitive) | `name:like:ANC` |
| `ilike` / `!ilike` | case-insensitive LIKE | `name:ilike:malaria` |
| `in:[a,b,c]` | property in set | `id:in:[abc,def]` |
| `!in:[a,b]` | property NOT in set | `code:!in:[X,Y]` |
| `null` / `!null` | null / non-null | `description:null` |
| `empty` / `!empty` | empty string | `code:empty` |
| `token` / `!token` | token-match (whitespace-split) | `name:token:malaria cases` |

Combine via repeated `--filter`:

```bash
dhis2 metadata list dataElements \
  --filter "valueType:eq:INTEGER_POSITIVE" \
  --filter "domainType:eq:AGGREGATE"
# AND by default — both must match
```

Or OR:

```bash
dhis2 metadata list dataElements \
  --filter "name:like:ANC" \
  --filter "code:eq:DEancVisit1" \
  --root-junction OR
# either match is enough
```

Nested-property filters work too: `children.name:like:x`.

## Field selector

Plain, preset, nested, and transformed:

| Shape | Example | Resolves to |
| --- | --- | --- |
| Plain | `id,name,code` | those three fields |
| Preset | `:identifiable` | `id,name,code,created,lastUpdated,displayName` |
| Preset | `:nameable` | `:identifiable` + `shortName`, `description` |
| Preset | `:owner` | every "owner"-category field for the resource |
| Preset | `:all` | every field on the object |
| Exclusion | `:all,!lastUpdated` | `:all` minus `lastUpdated` |
| Nested | `children[id,name,level]` | those fields inside each `children` entry |
| Rename | `displayName~rename(label)` | DHIS2 returns the field as `label` |

```bash
# Presets save typing for the common shapes
dhis2 metadata list dataElements --fields ":identifiable"

# Nested selector pulls a sub-tree
dhis2 metadata list organisationUnits --fields "id,name,children[id,name]"

# `:all,!<field>` excludes expensive fields
dhis2 metadata list dashboards --fields ":all,!dashboardItems"
```

## Pagination

| Mode | How | When to use |
| --- | --- | --- |
| Single page | `--page 1 --page-size 50` | Interactive use, top-N browsing. |
| Walk pages | `--page N` repeatedly | You control the iteration. |
| Stream all | `--all` | Full catalog dump; the service walks page=1,2,... internally. |

`--all` uses the service's `iter_metadata` async generator with `page_size=500` by default — large enough to keep request count low, small enough not to blow memory on heavy `:all` selectors.

## Localisation

```bash
dhis2 metadata list dataElements --translate --locale fr --fields ":identifiable"
# displayName returns the French translation when DHIS2 has one
```

## MCP example

```python
await mcp.call_tool("metadata_list", {
    "resource": "dataElements",
    "fields": ":identifiable",
    "filters": ["valueType:eq:INTEGER_POSITIVE", "domainType:eq:AGGREGATE"],
    "root_junction": "AND",
    "order": ["name:asc"],
    "page_size": 25,
    "translate": True,
    "locale": "fr",
})
# -> [{"id": "...", "name": "...", "code": "...", ...}, ...]
```

Agents pass `paging=False` (the default when `--all` is on at the CLI) to receive every row in one response.

## Why a dict return (not the pydantic model)

FastMCP can return pydantic models, but MCP agents consume JSON. `list[dict[str, Any]]` is the most portable shape. `_dump()` in the service uses `model_dump(by_alias=True, exclude_none=True, mode="json")` so datetimes, UUIDs, and nested refs serialise cleanly.

## Error handling

- Unknown resource → `UnknownResourceError` with a helpful message suggesting `list_resource_types`. Both CLI and MCP surface this as an actionable error.
- Server-side errors (403, 409, 500) propagate as `Dhis2ApiError` — FastMCP wraps them as tool-error results with the DHIS2 message body attached.
