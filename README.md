# dhis2-utils

DHIS2 tooling — a `uv` workspace containing a pure client library, a Typer CLI, a FastMCP server, a Playwright browser-automation helper, and a shared plugin runtime. DHIS2 v42 and v43, async throughout.

## Workspace members

| Package | Purpose | PyPI |
| --- | --- | --- |
| `dhis2-client` | Pure async httpx + pydantic DHIS2 client with pluggable auth (Basic, PAT, OAuth2/OIDC). Typed models from both `/api/schemas` and `/api/openapi.json` codegen. | publishable |
| `dhis2-codegen` | Generator that emits pydantic models + `StrEnum`s + CRUD accessors into `dhis2_client.generated.v{N}/`. Two source-of-truth paths: `/api/schemas` for metadata resources, `/api/openapi.json` for instance-side shapes (tracker writes, envelopes, auth schemes). | private |
| `dhis2-core` | Shared runtime: profile discovery, plugin registry, auth factory, token store, first-party plugins. | private |
| `dhis2-cli` | Typer console script `dhis2`. | private |
| `dhis2-mcp` | FastMCP server `dhis2-mcp`. | private |
| `dhis2-browser` | Playwright helpers for DHIS2 UI automation — PAT minting, Playwright-driven OIDC login + consent (`drive_oauth2_login` / `drive_login_form`), dashboard / viz / map screenshot capture. Mounted as the `dhis2 browser` sub-app when the `[browser]` extra is installed. | private |

## CLI surface

Sixteen top-level domains; every plugin shares a `service.py` between the CLI and MCP sides so one typed call answers both surfaces.

| Command | What it covers |
| --- | --- |
| `dhis2 profile` | Manage DHIS2 profiles (Basic / PAT / OAuth2) + the default precedence chain |
| `dhis2 system` | `/api/system/info`, `/api/me`, minted UIDs |
| `dhis2 metadata` | List / get / export / import any metadata resource, with DHIS2's full filter + fields selector |
| `dhis2 data` | Aggregate data values + tracker reads + pushes |
| `dhis2 analytics` | Aggregated, event, enrollment, outlier-detection, and tracked-entity analytics + table rebuild |
| `dhis2 user` | List / get / me / invite / reinvite / reset-password |
| `dhis2 user-group` / `dhis2 user-role` | Membership + authority administration |
| `dhis2 route` | Integration routes (`/api/routes`) — register, run, inspect |
| `dhis2 maintenance` | Background tasks, cache clear, data-integrity, soft-delete cleanup, validation-rule runs, predictor runs, analytics-table refresh |
| `dhis2 files` | `/api/documents` + `/api/fileResources` — upload / download / list binary attachments |
| `dhis2 messaging` | `/api/messageConversations` — send, reply, list, mark read/unread |
| `dhis2 apps` | `/api/apps` + `/api/appHub` — install / uninstall / update installed apps, browse the App Hub catalog, point DHIS2 at a custom App Hub |
| `dhis2 doctor` | One-command preflight — ~100 metadata-health + integrity checks against a live instance |
| `dhis2 browser` | Playwright-driven UI automation (PAT minting, dashboard / viz / map screenshot capture, automated OIDC login) — only registers when the `[browser]` extra is installed |
| `dhis2 dev` | Codegen, UID gen, PAT / OAuth2 seed helpers, branding (`dev customize`), sample data |

Full per-command reference: `uv run dhis2 --help`.

## Quick start

```bash
make install      # sync workspace deps
make lint         # ruff + mypy + pyright
make test         # pytest across all members
make docs-serve   # local mkdocs-material

# Bring up a fully-seeded DHIS2 v42 on :8080 (restores the committed e2e dump)
make dhis2-run
```

## Connecting to a DHIS2 instance

See [`docs/guides/connecting-to-dhis2.md`](docs/guides/connecting-to-dhis2.md) for the full end-to-end walkthrough covering Basic, PAT, and OAuth2/OIDC — including the `dhis.conf` keys the OAuth2 path needs on the DHIS2 server, manual OAuth2 client registration without the seed script, the `openId` user field, and a troubleshooting matrix of every failure mode.

For Python scripts, the canonical pattern is:

```python
from dhis2_core.client_context import open_client
from dhis2_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    me = await client.system.me()
    print(me.username)
```

The profile layer walks `DHIS2_PROFILE` env → `./.dhis2/profiles.toml` → `~/.config/dhis2/profiles.toml`. PyPI consumers who want the pure library without the profile layer can construct `Dhis2Client(url, auth=BasicAuth(...))` directly — see `examples/client/library_only_auth.py`.

## Documentation + examples

- Architecture + plugin walkthroughs: `docs/architecture/`
- API reference (mkdocstrings-rendered): `docs/api/`
- Roadmap: [`docs/roadmap.md`](docs/roadmap.md)
- Upstream DHIS2 quirks we've tripped over: [`BUGS.md`](BUGS.md)
- Runnable examples: `examples/cli/`, `examples/client/`, `examples/mcp/` (one script per feature)

Hard requirements, conventions, and the plugin / auth / workspace model are documented in `CLAUDE.md` and the `docs/` site.
