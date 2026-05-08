# dhis2w

A Python toolkit for DHIS2 — pure client library, CLI, MCP server, Playwright browser automation, and a shared plugin runtime, all in one `uv` workspace. Targets DHIS2 v42 and v43.

The repo lives at `winterop-com/dhis2w-utils`; PyPI ships the five publishable members under the `dhis2w-*` prefix. Not affiliated with DHIS2.

## Workspace members

| Package | PyPI | Purpose |
| --- | --- | --- |
| [`dhis2w-client`](https://pypi.org/project/dhis2w-client/) | `pip install dhis2w-client` | Pure async httpx + pydantic DHIS2 client with pluggable auth (Basic, PAT, OAuth2/OIDC). Typed models from both `/api/schemas` and `/api/openapi.json` codegen. |
| [`dhis2w-core`](https://pypi.org/project/dhis2w-core/) | `pip install dhis2w-core` | Shared runtime: profile discovery, plugin registry, auth factory, token store, first-party plugins. |
| [`dhis2w-cli`](https://pypi.org/project/dhis2w-cli/) | `pip install dhis2w-cli` | Typer console script `dhis2`. |
| [`dhis2w-mcp`](https://pypi.org/project/dhis2w-mcp/) | `pip install dhis2w-mcp` | FastMCP server `dhis2-mcp`. |
| [`dhis2w-browser`](https://pypi.org/project/dhis2w-browser/) | `pip install dhis2w-browser` | Playwright helpers for DHIS2 UI automation — PAT minting, Playwright-driven OIDC login + consent, dashboard / viz / map screenshot capture. Mounted under `dhis2 browser` when the `[browser]` extra is installed on `dhis2w-cli`. |
| `dhis2w-codegen` | _workspace-only_ | Generator that emits pydantic models + `StrEnum`s + CRUD accessors into `dhis2w_client.generated.v{N}/`. Two source-of-truth paths: `/api/schemas` for metadata resources, `/api/openapi.json` for instance-side shapes (tracker writes, envelopes, auth schemes). |

All five publishable packages release together (lockstep versioning); see [`docs/releasing.md`](docs/releasing.md).

## Install

### Use the CLI

The CLI command is named **`dhis2`** but the PyPI distribution is **`dhis2w-cli`** — that's why every install command spells out the package name explicitly.

```bash
# Install once, run forever — drops `dhis2` on $PATH
uv tool install dhis2w-cli

# With Playwright UI automation (browser screenshots, OIDC login, PAT minting)
uv tool install 'dhis2w-cli[browser]'
playwright install chromium    # one-time, after the install above

# Update to the latest release
uv tool upgrade dhis2w-cli

# Force a re-install (handy after PyPI publish issues / cache problems)
uv tool install --reinstall dhis2w-cli

# Check what's installed
uv tool list

# Remove
uv tool uninstall dhis2w-cli
```

After `uv tool install dhis2w-cli`, run the CLI directly:

```bash
dhis2 --help
dhis2 system info --url https://play.im.dhis2.org/dev-2-43 --username admin --password district
```

#### One-shot runs without installing — `uvx`

`uvx` is uv's "run-and-forget" runner — it fetches the package into a cache and runs the binary, with no permanent install:

```bash
# uvx <command>           # works when the binary name == the package name
# uvx --from <pkg> <cmd>  # required when they differ — that's our case

uvx --from dhis2w-cli dhis2 --help
uvx --from dhis2w-cli dhis2 system info --url https://play.im.dhis2.org/dev-2-43 --username admin --password district

# With the browser extra
uvx --from 'dhis2w-cli[browser]' dhis2 browser pat --url ...

# Force a cache refresh — pulls the latest published version
uvx --refresh --from dhis2w-cli dhis2 --help
```

`pip install dhis2w-cli` works the same way if you prefer pip — `uv tool install` just isolates the install in its own venv so it can't conflict with project deps.

### Use the client library in your own project

```bash
# Inside a uv-managed project
uv add dhis2w-client

# Or with pip
pip install dhis2w-client
```

```python
from dhis2w_client import BasicAuth, Dhis2Client

async with Dhis2Client(
    base_url="https://play.im.dhis2.org/dev-2-43",
    auth=BasicAuth(username="admin", password="district"),
) as client:
    me = await client.system.me()
    print(me.username)
```

`dhis2w-client` is standalone — no dependency on `dhis2w-core` or the profile system. PyPI users who want the typed async client + generated metadata models stop here.

### Use the MCP server

`dhis2w-mcp` exposes ~336 typed tools (one per CLI command) over the MCP stdio transport. Connect any MCP host — Claude Desktop, Claude Code, Cursor, or anything that speaks stdio MCP.

The PyPI distribution name **is** the binary name here (`dhis2w-mcp`), so the `--from` dance isn't needed:

```bash
# Install once — drops `dhis2w-mcp` on $PATH
uv tool install dhis2w-mcp

# Update later
uv tool upgrade dhis2w-mcp

# Or run on demand without installing
uvx dhis2w-mcp

# Force a fresh fetch (after a new PyPI release)
uvx --refresh dhis2w-mcp
```

**Claude Desktop** — edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "dhis2": {
      "command": "uvx",
      "args": ["dhis2w-mcp"],
      "env": {
        "DHIS2_URL": "https://play.im.dhis2.org/dev-2-43",
        "DHIS2_USERNAME": "admin",
        "DHIS2_PASSWORD": "district"
      }
    }
  }
}
```

Restart Claude Desktop. PAT auth works the same way — replace the username/password pair with `"DHIS2_PAT": "d2p_..."`.

**Claude Code** — register from any shell:

```bash
claude mcp add dhis2 -s user \
  -e DHIS2_URL=https://play.im.dhis2.org/dev-2-43 \
  -e DHIS2_PAT=d2p_... \
  -- uvx dhis2w-mcp
```

`-s user` makes the server available across every project. Tools land in-session as `mcp__dhis2__system_whoami`, `mcp__dhis2__metadata_data_element_list`, etc.

**Cursor** — edit `~/.cursor/mcp.json` with the same JSON shape as Claude Desktop and reload.

The full per-client setup, profile-based auth (`.dhis2/profiles.toml` for OAuth2 / OIDC), tool-naming convention, and troubleshooting are in [`packages/dhis2w-mcp/README.md`](packages/dhis2w-mcp/README.md).

### Use the profile layer (env / TOML config)

The `dhis2w-cli` and `dhis2w-mcp` packages share a profile system that walks `DHIS2_PROFILE` env → `./.dhis2/profiles.toml` → `~/.config/dhis2/profiles.toml`:

```bash
# One-shot bootstrap: prompts for URL + auth, saves a profile
dhis2 profile bootstrap mywork

# List what's known
dhis2 profile list

# Switch the default
dhis2 profile default mywork
```

```python
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    me = await client.system.me()
    print(me.username)
```

PyPI consumers who want the library without the profile layer can construct `Dhis2Client(url, auth=BasicAuth(...))` directly — see `examples/client/library_only_auth.py`.

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

Full per-command reference: `dhis2 --help` (or `uvx dhis2w-cli --help`).

## Working on the workspace itself

```bash
git clone git@github.com:winterop-com/dhis2w-utils.git
cd dhis2w-utils

make install      # sync workspace deps (uv sync --all-packages --all-extras)
make lint         # ruff + mypy + pyright
make test         # pytest across all members
make docs-serve   # local mkdocs-material

# Bring up a fully-seeded DHIS2 v43 on :8080 (Flyway-bootstraps; v42 still has a seeded e2e dump)
make dhis2-run

# Refresh codegen against the public play instances (no docker needed)
make dhis2-codegen-play
```

## Connecting to a DHIS2 instance

See [`docs/guides/connecting-to-dhis2.md`](docs/guides/connecting-to-dhis2.md) for the full end-to-end walkthrough covering Basic, PAT, and OAuth2/OIDC — including the `dhis.conf` keys the OAuth2 path needs on the DHIS2 server, manual OAuth2 client registration without the seed script, the `openId` user field, and a troubleshooting matrix of every failure mode.

## Documentation + examples

- Architecture + plugin walkthroughs: `docs/architecture/`
- API reference (mkdocstrings-rendered): `docs/api/`
- Releasing: [`docs/releasing.md`](docs/releasing.md)
- Roadmap: [`docs/roadmap.md`](docs/roadmap.md)
- Upstream DHIS2 quirks we've tripped over: [`BUGS.md`](BUGS.md)
- Runnable examples: `examples/cli/`, `examples/client/`, `examples/mcp/` (one script per feature)

Hard requirements, conventions, and the plugin / auth / workspace model are documented in `CLAUDE.md` and the `docs/` site.
