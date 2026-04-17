# Architecture overview

`dhis2-utils` is designed around **three orthogonal axes of extensibility**. Extending one should never force edits to another — that's how we keep this codebase maintainable as it grows.

## The three axes

### 1. Workspace members (shipping units)

Each shippable unit of code is a `uv` workspace member under `packages/`:

| Member | Role |
| --- | --- |
| `dhis2-client` | Pure async DHIS2 API client. PyPI-publishable. |
| `dhis2-core` | Profile system, plugin registry, first-party plugins. |
| `dhis2-cli` | Thin Typer console-script shell. |
| `dhis2-mcp` | Thin FastMCP server shell. |
| `dhis2-browser` | Playwright helpers for UI automation. |
| `dhis2-codegen` | Version-aware client generator. |

New surfaces (a future FastAPI web UI, an HTTP webhook receiver, a TUI) land as new members. No edits required to existing ones.

### 2. Plugins inside `dhis2-core`

Each DHIS2 domain (metadata, tracker, analytics, screenshots, indicator validation, …) is a self-contained plugin package in `dhis2-core/src/dhis2_core/plugins/<name>/`. Every plugin is a folder with this shape:

```
<name>/
├── __init__.py        # exports `plugin = Plugin(name="<name>", ...)`
├── models.py          # plugin-internal pydantic view-models (reports, summaries, job state)
├── service.py         # async pure functions — single source of truth for the domain
├── cli.py             # Typer sub-app wrapping service.py
├── mcp.py             # FastMCP tool registrations wrapping service.py
└── tests/
```

The CLI and MCP surfaces both call into the same `service.py`. They never drift out of parity because neither is primary.

Plugins are discovered two ways:

- **Built-ins** — iterate `dhis2_core.plugins.*` at startup.
- **External** — `importlib.metadata.entry_points(group="dhis2.plugins")`. An external package (like `dhis2-codegen`) can add commands/tools without a PR.

### 3. Auth providers inside `dhis2-client`

`dhis2-client` defines an `AuthProvider` Protocol. The client never touches auth internals — it just asks for headers. Three providers ship in-box: `BasicAuth`, `PatAuth`, `OAuth2Auth`. Future providers (service-account JWT, OIDC federation, proxy-injected headers) land as new files in `dhis2-client/auth/` without touching `client.py`.

## Dependency arrows

```
dhis2-browser  ─►  dhis2-client
dhis2-core     ─►  dhis2-client
dhis2-cli      ─►  dhis2-core    (─► dhis2-browser as optional extra)
dhis2-mcp      ─►  dhis2-core    (─► dhis2-browser as optional extra)
dhis2-codegen  ─►  dhis2-client
```

No cycles. `dhis2-client` is the foundation everything builds on, which is what lets it ship to PyPI independently.

## Why this matters

Every time a new requirement comes in, we should be able to say "that's a plugin", "that's a new auth provider", or "that's a new workspace member" — and build it in isolation. If a new requirement forces edits across three members, the architecture is wrong.
