# dhis2-utils

Private DHIS2 tooling — a `uv` workspace with a pure client library, a Typer CLI, a FastMCP server, a Playwright browser-automation helper, a code generator, and a shared plugin runtime.

## Where to start

- **Architecture** — the thinking behind the shape of this repo. Start with [Overview](architecture/overview.md).
- **Codegen** — how the version-aware generated clients are produced and why [Codegen](codegen.md).
- **Decisions log** — running list of architectural choices with their rationale [Decisions](decisions.md).

## Quick reference

| Package | What it is | PyPI |
| --- | --- | --- |
| `dhis2-client` | Async DHIS2 API client with pluggable auth and pydantic models | publishable |
| `dhis2-core` | Profile discovery, plugin registry, first-party plugins | private |
| `dhis2-cli` | Typer console script `dhis2` (mounts plugins from `dhis2-core`) | private |
| `dhis2-mcp` | FastMCP server `dhis2-mcp` (mounts the same plugins) | private |
| `dhis2-browser` | Playwright helpers (PAT creation, future UI automation) | private |
| `dhis2-codegen` | Version-aware client generator | private |

Plus `infra/` — docker-compose stack for running a local DHIS2 instance with pre-seeded PATs + OAuth2 client.

## Capability matrix

| Domain | CLI | MCP | Docs |
| --- | --- | --- | --- |
| Profile (list/verify/switch/add/remove/show) | `dhis2 profile` | 4 read-only tools | [link](architecture/profiles.md) |
| System (whoami, info) | `dhis2 system` | 2 tools | [link](architecture/system.md) |
| Metadata (119 generated CRUD resources) | `dhis2 metadata` | 3 tools | [link](architecture/metadata-plugin.md) |
| Aggregate (dataValueSets, dataValues) | `dhis2 aggregate` | 4 tools | [link](architecture/aggregate.md) |
| Tracker (TE, enrollments, events, relationships, bulk) | `dhis2 tracker` | 6 tools | [link](architecture/tracker.md) |
| Analytics (aggregated, raw, dataValueSet, refresh) | `dhis2 analytics` | 4 tools | [link](architecture/analytics.md) |
| Codegen (dhis2-codegen entry point) | `dhis2 codegen` | — | [link](codegen.md) |
| Playwright PAT | `dhis2-browser pat` | — | [link](pat-helper.md) |

**Total MCP surface: 23 tools. Every domain tool accepts an optional `profile: str | None` kwarg so an agent can target any configured profile per call.**

Day-to-day workflows (`make install`, `make lint`, `make test`, `make docs-serve`) are documented in the repo root `README.md`.
