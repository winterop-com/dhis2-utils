# Architecture overview

`dhis2w-utils` is designed around **three orthogonal axes of extensibility**. Extending one should never force edits to another — that's how we keep this codebase maintainable as it grows.

## The three axes

### 1. Workspace members (shipping units)

Each shippable unit of code is a `uv` workspace member under `packages/`:

| Member | Role | PyPI |
| --- | --- | --- |
| `dhis2w-client` | Pure async DHIS2 API client. | [`dhis2w-client`](https://pypi.org/project/dhis2w-client/) |
| `dhis2w-core` | Profile system, plugin registry, first-party plugins. | [`dhis2w-core`](https://pypi.org/project/dhis2w-core/) |
| `dhis2w-cli` | Thin Typer console-script shell. | [`dhis2w-cli`](https://pypi.org/project/dhis2w-cli/) |
| `dhis2w-mcp` | Thin FastMCP server shell. | [`dhis2w-mcp`](https://pypi.org/project/dhis2w-mcp/) |
| `dhis2w-browser` | Playwright helpers for UI automation. | [`dhis2w-browser`](https://pypi.org/project/dhis2w-browser/) |
| `dhis2w-codegen` | Version-aware client generator. | _workspace-only_ |

New surfaces (a future FastAPI web UI, an HTTP webhook receiver, a TUI) land as new members. No edits required to existing ones.

### 2. Plugins inside `dhis2w-core`

Each DHIS2 domain (metadata, tracker, analytics, screenshots, indicator validation, …) is a self-contained plugin package in `dhis2w-core/src/dhis2w_core/plugins/<name>/`. Every plugin is a folder with this shape:

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

- **Built-ins** — iterate `dhis2w_core.plugins.*` at startup.
- **External** — `importlib.metadata.entry_points(group="dhis2.plugins")`. An external package (like `dhis2w-codegen`) can add commands/tools without a PR.

### 3. Auth providers inside `dhis2w-client`

`dhis2w-client` defines an `AuthProvider` Protocol. The client never touches auth internals — it just asks for headers. Three providers ship in-box: `BasicAuth`, `PatAuth`, `OAuth2Auth`. Future providers (service-account JWT, OIDC federation, proxy-injected headers) land as new files in `dhis2w-client/auth/` without touching `client.py`.

## Dependency arrows

```
dhis2w-browser  ─►  dhis2w-client
dhis2w-core     ─►  dhis2w-client
dhis2w-cli      ─►  dhis2w-core    (─► dhis2w-browser as optional extra)
dhis2w-mcp      ─►  dhis2w-core    (─► dhis2w-browser as optional extra)
dhis2w-codegen  ─►  dhis2w-client
```

No cycles. `dhis2w-client` is the foundation everything builds on, which is what lets it ship to PyPI independently.

## Why this matters

Every time a new requirement comes in, we should be able to say "that's a plugin", "that's a new auth provider", or "that's a new workspace member" — and build it in isolation. If a new requirement forces edits across three members, the architecture is wrong.
