# Client examples

Python library usage — `dhis2w-client` + `dhis2w-core.open_client()` — for callers embedding the DHIS2 client inside a larger application. Every example reads the active DHIS2 profile (via env or TOML) and runs end-to-end against a seeded v42 stack.

> **Canonical catalogue**: [`docs/examples.md`](../../docs/examples.md) — full catalogue of every example across CLI / client / MCP with links to the concept docs that explain each one.

## Prerequisites

```bash
make dhis2-run                                       # DHIS2 + seeded auth
set -a; source infra/home/credentials/.env.auth; set +a

# Create a profile once — examples resolve it automatically via DHIS2_PROFILE / TOML discovery.
dhis2 profile add local --url http://localhost:8080 --auth pat --default --verify
```

## Running one

```bash
uv run python examples/client/whoami.py
```

Examples that need `DHIS2_OAUTH_*` env (the OIDC flow) say so in their docstring.

## Entry points

- `dhis2w_client.Dhis2Client(url, auth)` — the raw async client. Every example that doesn't need profiles goes through this.
- `dhis2w_core.client_context.open_client(profile)` — profile-aware context manager. Most examples use this because it picks up the seeded credentials.
- `dhis2w_core.plugins.<name>.service.*` — service-layer functions for operations that have a typed CLI/MCP surface (metadata import/diff/patch, user admin, ...). See `metadata_export_import.py` / `metadata_diff.py` / `metadata_patch.py` for the pattern.

See the [client library tutorial](../../docs/guides/client-tutorial.md) for a narrative walkthrough of the main entry points.

## v42 vs v43 schemas

DHIS2 v42 and v43 differ in a handful of resource shapes — `DashboardItem.user` becomes `users`, `TrackedEntityAttribute.favorite` becomes `favorites`, `Section.user` and `Program.favorite` are removed, three top-level resources are dropped, and ~20 new fields appear across Program / EventVisualization / Map / TrackedEntityAttribute. The full per-resource diff is at [`docs/architecture/schema-diff-v42-v43.md`](../../docs/architecture/schema-diff-v42-v43.md); the narrative + access patterns are at [`docs/architecture/versioning.md`](../../docs/architecture/versioning.md).

One runnable example per changed schema, prefixed `v43_` so it's clear which version each one targets:

| Example | Schema / change kind |
| --- | --- |
| `v43_dashboard_item_users.py` | `DashboardItem.user` -> `users` (rename + reshape: `Reference` -> `list[User]`) |
| `v43_tracked_entity_attribute_favorites.py` | `TrackedEntityAttribute.favorite` -> `favorites` (rename + reshape) + 6 new search fields |
| `v43_program_change_log_and_labels.py` | `Program` v43 additions: `enableChangeLog`, `enrollmentCategoryCombo`, 4 label-pair fields. Plus `Program.favorite` removed. |
| `v43_event_visualization_fix_headers.py` | `EventChart` / `EventReport` / `EventVisualization` add `fixColumnHeaders`, `fixRowHeaders`, `hideEmptyColumns` |
| `v43_map_basemaps.py` | `Map.basemaps` v43-only addition (collection of `Basemap`) |
| `v43_section_user_removed.py` | `Section.user` removed in v43 (also `Section.favorite`) |
| `v43_removed_resources.py` | `pushAnalysis`, `externalFileResource`, `dataInputPeriods` removed in v43 |
