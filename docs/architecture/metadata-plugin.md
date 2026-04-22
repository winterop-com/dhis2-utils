# Metadata plugin

`dhis2-core/plugins/metadata/` wraps the generated CRUD resources in a uniform CLI + MCP surface. It's a thin layer — the real work is in the generated `client.resources.<name>` accessors (see [Metadata CRUD](metadata-crud.md) for the underlying resources, [Plugin runtime](plugins.md) for the mounting pattern).

## What it exposes

Three operations, available as both CLI subcommands and MCP tools:

| Operation | CLI | MCP tool |
| --- | --- | --- |
| List available resource types | `dhis2 metadata type list` | `metadata_type_list` |
| List instances of one type | `dhis2 metadata list <resource>` | `metadata_list` |
| Fetch one by UID | `dhis2 metadata get <resource> <uid>` | `metadata_get` |
| Patch an object (RFC 6902) | `dhis2 metadata patch <resource> <uid>` | `metadata_patch` |
| Export a bundle | `dhis2 metadata export` | `metadata_export` |
| Import a bundle | `dhis2 metadata import FILE` | `metadata_import` |
| Diff two bundles (or bundle vs live) | `dhis2 metadata diff A B [--live]` | `metadata_diff` |
| Diff two profiles (staging vs prod drift) | `dhis2 metadata diff-profiles A B -r <resource>` | `metadata_diff_profiles` |

The `<resource>` argument is DHIS2's camelCase plural — `dataElements`, `indicators`, `organisationUnits`, `dashboards`, `dataSets`. The plugin maps it to the Resources attribute (`data_elements`, etc.) via a tiny camel-to-snake helper.

## `metadata list` — full flag surface

Every DHIS2 `/api/<resource>` query parameter is exposed:

| Flag | DHIS2 param | Example | Notes |
| --- | --- | --- | --- |
| `--fields` | `fields=` | `--fields ":identifiable"` | See [Field selector](#field-selector). |
| `--filter` | `filter=` | `--filter "name:like:Penta"` | Repeatable. See [Filter syntax](#filter-syntax). |
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
| `eq` | equals | `code:eq:DE_PENTA1` |
| `!eq` / `ne` | not equal | `code:!eq:REFERENCE` |
| `gt`, `ge`, `lt`, `le` | numeric/date compare | `created:ge:2024-01-01` |
| `like` / `!like` | SQL LIKE (case-sensitive) | `name:like:Penta` |
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
  --filter "name:like:Penta" \
  --filter "code:eq:DE_PENTA1" \
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

## Typed surface all the way through

The plugin returns typed pydantic models at every service boundary; the
JSON-shaped `dict` only appears at the two edges that actually need it —
the HTTP wire (going in and out of DHIS2) and the MCP/CLI serialisation
edge (where the output format is text). Every other layer is typed.

| Service function | Return type |
| --- | --- |
| `list_metadata(...)` | `list[<GeneratedModel>]` (e.g. `list[DataElement]`) |
| `get_metadata(...)` | `<GeneratedModel>` |
| `iter_metadata(...)` | `AsyncIterator[<GeneratedModel>]` |
| `export_metadata(...)` | `MetadataBundle` |
| `diff_bundles(left, right)` | `MetadataDiff` (takes `MetadataBundle` on both sides) |
| `bundle_dangling_references(bundle)` | `DanglingReferences` |
| `import_metadata(profile, bundle)` | `WebMessageResponse` (takes `MetadataBundle`) |

### `MetadataBundle`

`dhis2_core.plugins.metadata.models.MetadataBundle` wraps a DHIS2
`GET /api/metadata` response. DHIS2's top-level keys come in two shapes —
meta (`system`, `date`) and dynamic resource collections (`dataElements`,
`indicators`, ...). `MetadataBundle` exposes the meta keys as typed
nullable slots and the resource collections via typed accessor methods:

```python
from dhis2_core.plugins.metadata.models import MetadataBundle

# Build from a raw /api/metadata response (or JSON on disk):
bundle = MetadataBundle.from_raw(json.loads(path.read_text()))

# Iterate resource collections:
for resource_name, items in bundle.resources():
    for item in items:
        print(item.id, item.name)  # typed id + name

# Helpers:
bundle.all_uids()       # set[str] — every top-level UID
bundle.summary()        # {dataElements: 12, indicators: 3, ...}
bundle.total()          # total object count
bundle.get_resource("dataElements")   # list[MetadataItem] or []
bundle.has_resource("options")        # bool
```

Each item is a `MetadataItem` — `extra="allow"` pydantic model with typed
`id` + `name` plus every other DHIS2 field preserved. Nested references
inside an item (e.g. `categoryCombo: {id: ...}`) stay as bounded dicts in
`model_extra`; the rule carveout lets those bottom-layer refs exist
because they're only ever reached through typed accessors, never a
function's return type.

### Where dicts still appear (by design)

`list_metadata` / `get_metadata` return typed generated models; dumping
to JSON happens at the MCP tool edge (`_dump_model(...)`) and the CLI
JSON-output edge (`_dump_for_cli(...)`). Library callers get typed
models all the way through; agents get dicts.

The `POST /api/metadata` wire serialisation uses `bundle.to_wire()` which
returns a `dict[str, Any]` — consumed on the very next line by
`client.post_raw`. Same carveout as any `model_dump` call at an HTTP
boundary.

## Error handling

- Unknown resource → `UnknownResourceError` with a helpful message suggesting `list_resource_types`. Both CLI and MCP surface this as an actionable error.
- Server-side errors (403, 409, 500) propagate as `Dhis2ApiError` — FastMCP wraps them as tool-error results with the DHIS2 message body attached.

## Patch — partial updates via RFC 6902 JSON Patch

`dhis2 metadata patch <resource> <uid>` applies an RFC 6902 JSON Patch to a
single metadata object. DHIS2 accepts `PATCH /api/<resource>/{uid}` on every
metadata type — much lighter than round-tripping the full object via PUT
when you only need to change a handful of fields.

### Two input modes

**Inline:** `--set path=value` and `--remove path` are both repeatable and
combine into a single patch array on the wire. Values are JSON-decoded when
they parse as JSON, so booleans and numbers type through correctly:

```bash
dhis2 metadata patch dataElements fClA2Erf6IO \
  --set '/description=Renamed via CLI' \
  --set '/zeroIsSignificant=false' \
  --remove '/legacyField'
```

**File:** `--file patch.json` reads a full patch array on disk — every RFC
6902 op is accepted (`add`, `remove`, `replace`, `test`, `move`, `copy`):

```bash
cat > patch.json <<'JSON'
[
  {"op": "replace", "path": "/name", "value": "New name"},
  {"op": "copy", "path": "/shortName", "from": "/name"},
  {"op": "test", "path": "/valueType", "value": "INTEGER"}
]
JSON
dhis2 metadata patch dataElements fClA2Erf6IO --file patch.json
```

`--file` and `--set`/`--remove` are mutually exclusive (the CLI refuses
both in one call and refuses neither).

### Typed ops in Python code

Library callers skip the CLI and work with the discriminated `JsonPatchOp`
Union directly — every op is its own pydantic class with `extra="forbid"`
so wrong-shape payloads fail at construction time (a `RemoveOp` with a
`value` field is rejected before hitting DHIS2):

```python
from dhis2_client import AddOp, ReplaceOp, RemoveOp, MoveOp
from dhis2_core.plugins.metadata import service

# Typed ops — IDE autocomplete on every field, no stringly-typed `op` tag.
await service.patch_metadata(
    profile,
    "dataElements",
    "fClA2Erf6IO",
    [
        ReplaceOp(path="/description", value="Updated"),
        AddOp(path="/code", value="DE_PENTA_1"),
        RemoveOp(path="/legacyField"),
    ],
)

# Or go straight through the generated accessor (no service layer):
await client.resources.data_elements.patch(
    "fClA2Erf6IO",
    [ReplaceOp(path="/name", value="Renamed")],
)
```

Typed + dict ops mix freely — dicts route through `JsonPatchOpAdapter` on
the wire:

```python
await service.patch_metadata(
    profile,
    "dataElements",
    uid,
    [
        ReplaceOp(path="/description", value="Typed"),
        {"op": "add", "path": "/code", "value": "DICT_OP"},  # also accepted
    ],
)
```

### MCP

The `metadata_patch(resource, uid, ops)` tool accepts any list of
`{op, path, value?, from?}` dicts. The tool signature routes each op
through the adapter server-side, so agents get clear validation errors
instead of silent DHIS2 400s when they pass wrong-shape ops.

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

### Per-resource filters (narrow the export)

DHIS2's `/api/metadata` accepts per-resource filters and field selectors
via the `<resource>:filter=<expr>` / `<resource>:fields=<selector>` query
param form. Both are exposed:

```bash
# All dataElements whose name contains "Penta" AND valueType is INTEGER_POSITIVE,
# plus every indicator whose code starts with "HIV_":
dhis2 metadata export \
  --resource dataElements --resource indicators \
  --filter "dataElements:name:like:Penta" \
  --filter "dataElements:valueType:eq:INTEGER_POSITIVE" \
  --filter "indicators:code:like:HIV_" \
  --output slice.json

# Per-resource fields override: keep heavy `:owner` for dataElements, but only
# grab `:identifiable` for the large categoryCombos collection:
dhis2 metadata export \
  --resource dataElements --resource categoryCombos \
  --fields ":owner" \
  --resource-fields "dataElements::owner" \
  --resource-fields "categoryCombos::identifiable" \
  --output filtered.json
```

The filter DSL is identical to `dhis2 metadata list --filter`
([filter syntax](#filter-syntax)) — just prefixed with the resource name
and a colon. Repeated `--filter` values for the same resource are AND'd
server-side.

### Reference integrity (dangling-reference warning)

Narrowing an export by filter or resource type means your bundle can end
up with nested `{"id": "abc"}` references pointing at objects you didn't
include. `dhis2 metadata export` walks the downloaded bundle by default
and warns when this happens:

```
WARNING: 7 dangling reference(s) — UIDs referenced by objects in the bundle
but not present in the bundle itself.
  field             missing  sample UIDs
  categoryCombo     4        bjDvmb4bfuf, pA2tGE9o2o5, ... (+2 more)
  optionSet         2        PiZhoVG4Epg, XkQjnXmbpRG
  legendSets        1        PWpD1lcuIWn
Re-run with the referenced resource types added (e.g.
`--resource categoryCombos --resource optionSets`) or silence with
`--no-check-references`.
```

The walker groups by **reference field name** (the JSON key that held the
`{"id": "..."}`) so the user knows which resource type to add. It skips a
curated noise list by default — `createdBy`, `lastUpdatedBy`, `user`,
`userAccesses`, `userGroupAccesses`, `sharing` — because a metadata export
rarely includes the users DHIS2 refers to from those slots; including
them in the warning would drown the signal.

The programmatic API (`service.bundle_dangling_references(bundle)`) returns
a typed `DanglingReferences` model with `items` (per-field), `total_missing`,
`bundle_uid_count`, and an `is_clean` convenience flag — the same shape the
MCP `metadata_export` tool returns under `dangling_references` when
`check_references=True` (default).

Turn the check off with `--no-check-references` for scripted pipelines that
don't want the extra walk.

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

## `diff-profiles` — staging-vs-prod drift

`dhis2 metadata diff-profiles <a> <b>` exports the same resource slice from
two registered profiles concurrently and diffs them. Built for drift
monitoring between environments — staging and prod diverge by design on
user accounts, org-unit assignments, and incidental settings, so the
command REQUIRES a resource list and layers filters on top.

```bash
# Minimum: narrow to specific resource types (required).
dhis2 metadata diff-profiles stage prod -r dataElements -r indicators

# Per-resource filter — same `property:operator:value` DSL as
# `dhis2 metadata list --filter`, prefixed with the resource name:
dhis2 metadata diff-profiles stage prod \
  -r dataElements -r indicators \
  --filter 'dataElements:name:like:Penta' \
  --filter 'indicators:name:like:Penta'

# Extend the ignore list for cross-environment noise
# (sharing blocks and translations often differ without being "drift"):
dhis2 metadata diff-profiles stage prod -r dataElements \
  --ignore sharing --ignore translations

# CI shape: non-zero exit on any drift, JSON output for the alerting script.
dhis2 metadata diff-profiles stage prod -r dataElements \
  --exit-on-drift --json
```

The underlying engine (`service.diff_profiles`) fans out two
`export_metadata` calls via `asyncio.gather` so a slow staging instance
doesn't serialise with prod. Same filters are applied on both sides — what
you compare is always apples-to-apples.

MCP tool: `metadata_diff_profiles` (same shape; filters come in as
`per_resource_filters: {"resource": ["filter_expr", ...]}`).

The `examples/client/profile_drift_check.py` cookbook shows the Python
library path for the same pattern (useful when you want to post-process the
typed `MetadataDiff` before deciding what counts as real drift).
