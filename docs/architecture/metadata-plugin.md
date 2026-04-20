# Metadata plugin

`dhis2-core/plugins/metadata/` wraps the generated CRUD resources in a uniform CLI + MCP surface. It's a thin layer — the real work is in the generated `client.resources.<name>` accessors (see [Metadata CRUD](metadata-crud.md) for the underlying resources, [Plugin runtime](plugins.md) for the mounting pattern).

## What it exposes

Three operations, available as both CLI subcommands and MCP tools:

| Operation | CLI | MCP tool |
| --- | --- | --- |
| List available resource types | `dhis2 metadata type list` | `metadata_type_list` |
| List instances of one type | `dhis2 metadata list <resource>` | `metadata_list` |
| Fetch one by UID | `dhis2 metadata get <resource> <uid>` | `metadata_get` |
| Export a bundle | `dhis2 metadata export` | `metadata_export` |
| Import a bundle | `dhis2 metadata import FILE` | `metadata_import` |
| Diff two bundles (or bundle vs live) | `dhis2 metadata diff A B [--live]` | `metadata_diff` |

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

## Export / import

Round-trip metadata across instances with `dhis2 metadata export` and
`dhis2 metadata import` — two commands that together cover the
cross-environment dev workflow (copy a slice from a live instance to a
fresh stack, diff against upstream, or ship a reviewed bundle through CI).

### Export

`GET /api/metadata` with optional per-resource narrowing + DHIS2's standard
skip flags.

```bash
# Everything DHIS2 exports by default, lossless round-trip fields:
dhis2 metadata export --output full.json

# Narrow slice: dataElements + indicators, identifiable fields only:
dhis2 metadata export \
  --resource dataElements --resource indicators \
  --fields ":identifiable" --output slice.json

# Trim sharing blocks (useful when the target has different users/groups):
dhis2 metadata export --skip-sharing --output clean.json
```

The bundle summary (resource → count) prints to **stderr** so stdout stays
pipe-friendly (`dhis2 metadata export | jq ...` works). `--output FILE`
also prints the summary table + the total written.

**Default `fields=":owner"`.** This is the field preset DHIS2 itself uses
internally for cross-instance imports — every property required to
faithfully recreate the object on the target. Narrowing to `":identifiable"`
/ `"id,name"` is fine for inspection but fails on import because key fields
(category-combo references, sharing, etc.) are missing.

### Import

`POST /api/metadata` with typed flag surface for every DHIS2 import
parameter.

```bash
# Real import (upsert, atomic rollback on any failure):
dhis2 metadata import bundle.json

# Pre-check with DHIS2's validate mode — runs preheat + validation, commits nothing:
dhis2 metadata import bundle.json --dry-run

# Tighter strategy: CREATE only (fails if any object already exists):
dhis2 metadata import bundle.json --strategy CREATE --atomic-mode ALL

# Loose: keep going on individual failures, continue-on-error semantics:
dhis2 metadata import bundle.json --atomic-mode NONE

# Resolve references by CODE instead of UID (useful for bundles from a
# different instance where UIDs won't match):
dhis2 metadata import bundle.json --identifier CODE
```

`--dry-run` maps to DHIS2's `importMode=VALIDATE` — the server runs the full
validation + preheat pass but doesn't commit. The resulting report (via
`WebMessageResponse.import_count()` / `.conflicts()`) shows what *would*
happen.

Full flag surface mirrors DHIS2 1:1: `--strategy`, `--atomic-mode`,
`--identifier`, `--skip-sharing`, `--skip-translation`, `--skip-validation`,
`--merge-mode`, `--preheat-mode`, `--flush-mode`. Every option is a direct
pass-through; no workspace-invented defaults except `CREATE_AND_UPDATE` +
`ALL` (which match DHIS2's own defaults).

### Service / MCP

The same surface is reachable from the library:

```python
from dhis2_client import Dhis2Client
from dhis2_core.plugins.metadata import service

async with Dhis2Client(url, auth) as client:
    bundle = await service.export_metadata(
        profile, resources=["dataElements"], fields=":owner",
    )
    report = await service.import_metadata(
        profile, bundle, import_strategy="CREATE_AND_UPDATE", dry_run=True,
    )
    print(report.import_count())
```

MCP tools: `metadata_export` + `metadata_import`. Both accept a
`bundle_path` on disk so multi-megabyte bundles don't flow through the MCP
channel. See `examples/mcp/metadata_export_import.py` for the tool-call
form.

## Diff — preview before importing

`dhis2 metadata diff` compares two bundles structurally (or one bundle
against the live instance) and reports per-resource create / update / delete
counts. Use it as a safety gate before a real `metadata import` so you can
see exactly which objects get touched.

```bash
# File vs file — structural comparison of two exports:
dhis2 metadata diff baseline.json candidate.json

# File vs live instance — "what would change if I imported baseline.json?":
dhis2 metadata diff baseline.json --live

# Show up to 5 offending UIDs per resource row:
dhis2 metadata diff baseline.json candidate.json --show-uids

# JSON envelope, for piping into CI:
dhis2 metadata diff baseline.json candidate.json --json | jq '.total_updated'

# Custom ignore list: treat `code` changes as noise too:
dhis2 metadata diff a.json b.json --ignore code --ignore description
```

### What counts as a change

Objects are matched by `id` across the two bundles. Each pair goes into
exactly one bucket:

- **created** — UID present in `right` but not `left`.
- **deleted** — UID present in `left` but not `right`.
- **updated** — UID present in both, at least one non-ignored top-level field
  differs.
- **unchanged** — UID present in both, every comparable field matches.

### Default ignored fields

DHIS2 rewrites `lastUpdated`, `lastUpdatedBy`, `created`, `createdBy`,
`translations`, `access`, `favorites`, and `href` on every import — they
would otherwise dominate diff output with noise. They're skipped by default.
Add more via repeated `--ignore FIELD` (the defaults stay; your additions
extend the set).

### `--live` narrows the export

Passing `--live` exports only the resource types present in `left` — so a
bundle that contains just `dataElements` triggers a fetch of just
`/api/metadata?dataElements=true`, not the full catalog. That keeps the
diff fast enough for interactive use.

### Service / MCP

```python
from dhis2_core.plugins.metadata import service

diff = service.diff_bundles(left_bundle, right_bundle)
print(diff.total_created, diff.total_updated, diff.total_deleted)
for resource in diff.resources:
    for change in resource.updated:
        print(resource.resource, change.id, change.changed_fields)

# Or: file-on-disk vs live instance.
live_diff = await service.diff_bundle_against_instance(
    profile, bundle, bundle_label="baseline.json",
)
```

MCP tool: `metadata_diff` (pass `left_path` + `right_path`, or `left_path` +
`live=True`). See `examples/mcp/metadata_diff.py` and
`examples/client/metadata_diff.py` for worked calls.
