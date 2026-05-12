# dhis2w-core

Shared runtime for `dhis2w-cli` and `dhis2w-mcp`: profile discovery, plugin registry, auth factory, token store, and the first-party plugins (metadata, data, analytics, users, tracker, files, messaging, apps, route, maintenance, doctor, customize, system, profile, dev).

`dhis2w-core` is the bridge between `dhis2w-client` (the pure async API client) and the user-facing surfaces (CLI, MCP). End users typically don't install this directly — they install `dhis2w-cli` or `dhis2w-mcp` which pull `dhis2w-core` in transitively.

## Install

```bash
# Direct (rare — usually you want dhis2w-cli or dhis2w-mcp instead)
uv add dhis2w-core
```

## What's in the box

- **Profile system** — auto-discovers a profile from `.dhis2/profiles.toml` (CWD walk-up) or `~/.config/dhis2/profiles.toml`. `Profile` model + `profile_from_env()` env-var fallback.
- **Plugin registry** — walks `dhis2w_core.v{41,42,43}.plugins.*` plus `entry_points("dhis2.plugins")` for external plugins. Each plugin exposes `register_cli(app)` and `register_mcp(server)`.
- **Auth factory** — turns a `Profile` into the matching `AuthProvider` from `dhis2w-client`, wires the token store, manages OAuth2 PKCE redirect capture.
- **Token store** — SQLite-backed (`aiosqlite`) at `.dhis2/tokens.sqlite`, keyed by profile name.
- **`open_client(profile)` context manager** — the canonical "give me a connected client" entry point for plugin services.

## Plugins shipped

`metadata`, `data`, `analytics`, `tracker`, `user`, `user_group`, `user_role`, `route`, `apps`, `messaging`, `files`, `maintenance`, `doctor`, `customize`, `system`, `profile`, `dev`, `browser` (CLI-only, opt-in via `[browser]` extra).

Each plugin lives at `packages/dhis2w-core/src/dhis2w_core/plugins/<name>/` with `service.py` (typed business logic), `cli.py` (Typer commands), and `mcp.py` (FastMCP tools) — both surfaces call the same `service.py`.

## Documentation

Full architecture: https://winterop-com.github.io/dhis2w-utils/architecture/overview/.

`dhis2w-core` is one member of the [`dhis2w-utils`](https://github.com/winterop-com/dhis2w-utils) workspace.
