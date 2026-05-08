# dhis2-mcp

FastMCP server that exposes every `dhis2-core` plugin as MCP tools. Same service functions as the CLI; different I/O shape.

A connected agent (Claude Code, Cursor, etc.) sees ~336 typed tools grouped by plugin: `metadata_*`, `data_aggregate_*`, `data_tracker_*`, `analytics_*`, `route_*`, `user_*`, `apps_*`, `system_*`, `messaging_*`, `files_*`, `maintenance_*`, `customize_*`, `profile_*`, `doctor_*`.

## Install

The server is part of the `dhis2-utils` workspace. From a checkout of the repo:

```bash
uv sync --all-packages
```

This puts a `dhis2-mcp` console script on the workspace's path. `uv run dhis2-mcp` from anywhere inside the repo speaks MCP over stdio.

## Use with Claude Code

`claude mcp add` registers the server with the Claude Code CLI. Pick the option that matches how you want to maintain the install.

### Option 1 — point at the workspace (recommended for active development)

```bash
claude mcp add dhis2 -s user -- \
  uv run --directory /absolute/path/to/dhis2-utils dhis2-mcp
```

`uv run --directory` resolves the workspace from any cwd and uses the locked deps. `-s user` makes the server available across every Claude Code project; drop it for project-only.

### Option 2 — install as a standalone tool

```bash
uv tool install --from /absolute/path/to/dhis2-utils/packages/dhis2-mcp dhis2-mcp
claude mcp add dhis2 -s user -- dhis2-mcp
```

Puts a `dhis2-mcp` shim on your `PATH` so the Claude Code config doesn't reference the repo path. Trade-off: you have to `uv tool upgrade dhis2-mcp --reinstall` after pulling new commits.

### Pinning a profile

The server auto-discovers the active DHIS2 profile from `.dhis2/profiles.toml` (CWD walk-up) or `~/.config/dhis2/profiles.toml`. To pin one explicitly for the agent:

```bash
claude mcp add dhis2 -s user -e DHIS2_PROFILE=local_basic -- \
  uv run --directory /absolute/path/to/dhis2-utils dhis2-mcp
```

If no profile is configured, MCP tool calls fail with an actionable error pointing at `dhis2 init`.

### Verify

```bash
claude mcp list           # confirm 'dhis2' shows up
claude mcp get dhis2      # see the resolved command + env
```

Inside a Claude Code session the tools land as `mcp__dhis2__system_whoami`, `mcp__dhis2__metadata_data_element_list`, etc. The `mcp__dhis2__` prefix is added by Claude Code; the part after is the bare tool name registered by FastMCP.

### Picking up code changes

`uv run --directory ...` runs `uv sync` before launching the script (a fast no-op when nothing changed) and installs workspace packages in editable mode, so Python imports source files directly from `packages/dhis2-core/src/...`. There is no rebuild step:

| What you changed | What you have to do |
| --- | --- |
| Source code in `packages/*/src/...` (existing tools, new tools, new plugins, fixed bugs) | **Restart the MCP server** — end the Claude Code session and start a new one, or `/mcp` to reconnect. The new code is picked up automatically; `discover_plugins()` re-walks `dhis2_core.plugins.*` on each server start. |
| Added a new runtime dep (`uv add ...` from the repo root) | Nothing special. The lock file changes; next `uv run` re-syncs the venv before launching. |
| Moved the repo, changed the profile env var, or want to switch between Option 1 / Option 2 | **Re-run `claude mcp add`** (after `claude mcp remove dhis2`) — the invocation itself has to be re-recorded. |

The server is a long-lived process. Edits made while it's running are not visible until it restarts.

## Tool naming

All tools follow `<plugin>_<resource>_<verb>` in snake_case, verb-last:

```
metadata_data_element_list
metadata_data_element_get
metadata_data_element_create
user_role_authority_list
system_calendar_get
system_calendar_set
data_aggregate_push
```

See `docs/architecture/conventions.md` for the full verb table (list, get, create, delete, rename, update, patch, set, add_<thing>, remove_<thing>) and `docs/mcp-reference.md` for every tool with its parameter schema.

## Architecture

`dhis2-mcp` is a thin shell — it builds a `FastMCP` instance, walks every `dhis2_core.plugins.*` module, and calls each plugin's `register_mcp(server)`. Tool names, descriptions, and parameter schemas are derived from the registered Python function signatures + docstrings; return-type JSON schemas come from the annotated pydantic models. See `docs/architecture/mcp.md` for the deeper write-up.
