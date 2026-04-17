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
├── __init__.py          # version registry + loader
├── v40/__init__.py      # empty stub — run codegen against a v40 instance to populate
├── v41/__init__.py      # empty stub
├── v42/__init__.py      # empty stub
└── v43/__init__.py      # empty stub
```

Each `v{NN}/__init__.py` carries a `GENERATED: bool` flag. It starts `False`; codegen sets it `True` and writes model + resource modules alongside.

The generated code is **committed**, not gitignored. Diffs are reviewable in PRs — you can see when a new field appears on a resource, when an enum gains a constant, when an endpoint is removed.

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

## What happens in v43 when it ships

When DHIS2 ships 2.43:

1. Spin up a v43 instance (or use play when they publish a v43 build).
2. `make schemas URL=https://play.im.dhis2.org/stable-2-43-0 VERSION=v43` — or once profiles land, `make schemas PROFILE=v43-play`.
3. The generator populates `generated/v43/` with models + resources + a `schemas_manifest.json` snapshot.
4. `GENERATED = True` is stamped in the `__init__.py`.
5. Commit the generated files. The diff shows exactly what changed versus v42 — new types, new properties, removed endpoints.
6. `Dhis2Client.connect()` against v43 instances now auto-binds to the new module.

## Trade-offs

- **More code to review.** Every DHIS2 release produces a committed diff. That's the point — it's auditable — but it means the `generated/` folder grows with each version.
- **Committed generated code.** Some teams prefer gitignored generators. We don't — we want diffs reviewable, and we want `dhis2-client` to work on PyPI without users having to run codegen themselves.
- **One codegen per version, not per instance.** If two v42 instances have wildly different custom metadata, one of them will have models its code doesn't describe. We cover the standard schema; per-instance customization is not a goal of `dhis2-client` and probably belongs in a plugin.
- **Minor version only.** We key on `"v42"`, not `"2.42.1"`. Patch-level differences are not worth separate modules. If DHIS2 changes the schema mid-minor (which they shouldn't), we'd need to revisit.
