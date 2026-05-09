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

DHIS2 v42 and v43 differ in a handful of resource shapes — `DashboardItem.user` becomes `users`, `TrackedEntityAttribute.favorite` becomes `favorites`, `Section.user` and `Program.favorite` are removed, plus ~20 new fields. `version_aware_access.py` is the runnable demo of the three patterns for handling this (`client.version_key` branching, direct `dhis2w_client.generated.v43.*` imports, pinning via `version=Dhis2.V43`). See the full per-resource diff at [`docs/architecture/schema-diff-v42-v43.md`](../../docs/architecture/schema-diff-v42-v43.md) and the narrative at [`docs/architecture/versioning.md`](../../docs/architecture/versioning.md).
