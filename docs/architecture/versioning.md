# Version-aware generated clients

## URLs do not carry the version

DHIS2's API is always mounted at `/api/...`. Earlier DHIS2 releases exposed a versioned path variant (`/api/30/dataElements`); that's being phased out. Every URL this client constructs uses the plain `/api/{plural}` form.

Version-awareness therefore lives in the **payload shapes**, not the URLs. DHIS2 2.42 returns slightly different fields for (say) a `DataElement` than 2.44. Our generated pydantic models capture those differences per-version, and `Dhis2Client.connect()` picks the right module for whatever instance you're connected to.

## Why version-scoped models at all

DHIS2 schemas evolve across versions. New metadata types appear, existing types get new properties, enums pick up new constants. A single hand-curated client either gets out of date or lags behind the latest release.

Instead of fighting that, we lean in: each supported DHIS2 version gets its **own generated module** under `dhis2_client.generated.v{NN}`, produced by `dhis2 codegen` from that instance's `/api/schemas` endpoint.

## Layout

```
packages/dhis2-client/src/dhis2_client/generated/
├── __init__.py          # version registry + loader + Dhis2 enum
├── v40/                 # DHIS2 2.40.11 (125 schemas)
├── v41/                 # DHIS2 2.41.8 (125 schemas)
├── v42/                 # DHIS2 2.42.4 (119 schemas)
├── v43/                 # empty — dhis2/core:43 not yet on Docker Hub
└── v44/                 # rebuilt from committed manifest (116 schemas)
```

Each populated `v{NN}/` carries:

- `__init__.py` — sets `GENERATED = True` and re-exports every resource schema (`from dhis2_client.generated.v42 import DataElement`).
- `schemas/` — one pydantic `BaseModel` per DHIS2 metadata type, with `Field(description=...)` hints for owner/writable/bounds.
- `resources.py` — typed CRUD accessors (`client.resources.dataElements.get/list/create/update/delete`).
- `schemas_manifest.json` — snapshot of the `/api/schemas` response used at generation time. Committed so `dhis2 dev codegen rebuild` can regenerate offline.

The generated code is **committed**, not gitignored. Diffs are reviewable in PRs — you can see when a new field appears on a resource, when an enum gains a constant, when an endpoint is removed. The per-version `infra/dhis-{N}.sql.gz` dumps (Flyway-bootstrapped, no user data) sit alongside as cheap restore points.

## The `Dhis2` enum

`dhis2_client.Dhis2` is a `StrEnum` listing every version with a generated client — `Dhis2.V40` through `Dhis2.V44`. Two uses:

```python
from dhis2_client import Dhis2, Dhis2Client

# 1. Pin the version, skip auto-detection via /api/system/info.
async with Dhis2Client(url, auth=auth, version=Dhis2.V42) as client:
    ...

# 2. Direct schema import without the full path.
from dhis2_client.generated.v42 import DataElement, OrganisationUnit
```

## Runtime dispatch

On `Dhis2Client.connect()`:

1. `GET /api/system/info` → raw version string (e.g. `"2.42.0"`).
2. The minor component is extracted (e.g. `42`) and mapped to `"v42"`.
3. `dhis2_client.generated.available_versions()` is consulted — only populated versions (`GENERATED = True`) are candidates.
4. If `"v42"` is populated, that module is loaded and bound to `client.resources`, `client.models`, etc.
5. If `"v42"` is not populated and `allow_version_fallback=False` (default), `UnsupportedVersionError` is raised, pointing the user at `dhis2 codegen`.
6. If fallback is enabled, the nearest-lower populated version is chosen (e.g. `v41` for a v42 instance when only v40/v41 have been generated). Never picks a higher version.

```python
async with Dhis2Client(
    base_url="https://play.im.dhis2.org/stable-2-42-0",
    auth=BasicAuth("admin", "district"),
) as client:
    # client.version_key == "v42"
    # client.raw_version == "2.42.0"
    ...
```

## Why strict by default

When a user points at a v43 instance and only v40/v41/v42 are generated, the choice is:

- **Refuse** — force the user to run codegen against the live instance. Guarantees typing matches reality.
- **Fall back to v42** — v43-specific fields silently disappear; typed access to v42-known fields still works.
- **Runtime-generate** — build pydantic models on the fly from `/api/schemas`. Dynamic types, no static analysis, no IDE autocomplete. Rejected.

We default to "refuse" because a strict codebase that loudly fails when things are stale beats one that silently diverges. Opt-in soft fallback (`allow_version_fallback=True`) is there for CLIs and agents that want to keep working against unknown versions with a warning.

## Regenerating all versions

`make dhis2-codegen-all` (or the underlying `infra/scripts/codegen_all_versions.sh`) orchestrates the whole pipeline. Default set is `v42` — other versions are regenerated explicitly because their boots under arm64 emulation can race the compose healthcheck window:

```bash
infra/scripts/codegen_all_versions.sh 40 41 42   # explicit set
infra/scripts/codegen_all_versions.sh            # default — just v42
```

For each version N, the script:

1. Brings up a fresh `dhis2/core:N` stack with an empty-gzip placeholder where `infra/dhis.sql.gz` sits (so Flyway bootstraps a clean schema instead of trying to load a v42 dump into a v40 stack).
2. Waits for `/api/system/info` to respond.
3. Runs `dhis2 dev codegen generate` against `http://localhost:8080` with admin/district, which writes `generated/v{N}/schemas/`, `resources.py`, `__init__.py`, and `schemas_manifest.json`.
4. `pg_dump`s the post-Flyway schema into `infra/dhis-{N}.sql.gz` (excluding derived analytics_*, aggregated_*, completeness_*, and `_*` tables — those are regenerated by `analytics-trigger`).
5. Tears down, restores the committed dump.

Rebuilding from a committed manifest (no network) is cheap:

```bash
uv run dhis2 dev codegen rebuild                              # every v{N}/schemas_manifest.json
uv run dhis2 dev codegen rebuild --manifest path/to/foo.json  # just one
```

Useful after touching `emit.py` or the Jinja templates when you want every version refreshed without booting each server.

## What happens when a new DHIS2 version ships

1. Confirm the image is on Docker Hub: `docker pull dhis2/core:45`.
2. `infra/scripts/codegen_all_versions.sh 45` — boots the stack, runs codegen, dumps, tears down.
3. Add `V45 = "v45"` to the `Dhis2` enum in `dhis2_client.generated.__init__`.
4. Commit the new `generated/v45/` tree, `infra/dhis-45.sql.gz`, and the enum addition. Diff shows exactly what changed vs v44 — new types, new properties, removed endpoints.
5. `Dhis2Client.connect()` against v45 instances now auto-binds to the new module.

## Trade-offs

- **More code to review.** Every DHIS2 release produces a committed diff. That's the point — it's auditable — but it means the `generated/` folder grows with each version.
- **Committed generated code.** Some teams prefer gitignored generators. We don't — we want diffs reviewable, and we want `dhis2-client` to work on PyPI without users having to run codegen themselves.
- **One codegen per version, not per instance.** If two v42 instances have wildly different custom metadata, one of them will have models its code doesn't describe. We cover the standard schema; per-instance customization is not a goal of `dhis2-client` and probably belongs in a plugin.
- **Minor version only.** We key on `"v42"`, not `"2.42.1"`. Patch-level differences are not worth separate modules. If DHIS2 changes the schema mid-minor (which they shouldn't), we'd need to revisit.
