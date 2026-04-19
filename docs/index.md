# DHIS2 Utils

Python tooling for DHIS2. A `uv` workspace with an async client library, a Typer CLI, a FastMCP server, a Playwright browser helper, a code generator, and a shared plugin runtime.

## Where to start

- **New to the repo?** Skim the [Walkthrough](walkthrough.md), set up [a local DHIS2](local-setup.md), then pick a guide.
- **Writing Python that talks to DHIS2?** Read the [Python library tutorial](guides/client-tutorial.md). Every block is runnable.
- **Using the CLI?** [Connecting to DHIS2](guides/connecting-to-dhis2.md) covers Basic / PAT / OAuth2 setup with profiles.
- **Looking for the architecture?** Start at [Overview](architecture/overview.md), then [Typed schemas](architecture/typed-schemas.md) + [Codegen](codegen.md).
- **Browsing by symbol?** The [API reference](api/index.md) auto-renders every `dhis2-client` module's docstrings.

## Packages

| Package | Role | Published |
| --- | --- | --- |
| `dhis2-client` | Async DHIS2 API client with pluggable auth and pydantic models | publishable |
| `dhis2-core` | Profile discovery, plugin registry, first-party plugins | private |
| `dhis2-cli` | Typer console script `dhis2` (mounts plugins from `dhis2-core`) | private |
| `dhis2-mcp` | FastMCP server `dhis2-mcp` (mounts the same plugins) | private |
| `dhis2-browser` | Playwright helpers (PAT creation, future UI automation) | private |
| `dhis2-codegen` | Version-aware client generator | private |

Plus `infra/`, a docker-compose stack for running a local DHIS2 instance with pre-seeded PATs and an OAuth2 client.

## Capability matrix

| Domain | CLI | MCP | Docs |
| --- | --- | --- | --- |
| Profile (list/verify/show/default/add/remove/rename, login/logout/bootstrap) | `dhis2 profile` | 4 read-only tools | [Profiles](architecture/profiles.md) |
| System (whoami, info) | `dhis2 system` | 2 tools | [System module](architecture/system.md) |
| Metadata (type list + instance list/get on 119 resources) | `dhis2 metadata` | 3 tools | [Metadata plugin](architecture/metadata-plugin.md) |
| Data / aggregate (dataValueSets, dataValues) | `dhis2 data aggregate` | 4 tools | [Aggregate plugin](architecture/aggregate.md) |
| Data / tracker (entity/enrollment/event/relationship + push) | `dhis2 data tracker` | 6 tools | [Tracker plugin](architecture/tracker.md) |
| Analytics (query --shape table\|raw\|dvs, refresh) | `dhis2 analytics` | 2 tools | [Analytics plugin](architecture/analytics.md) |
| Route (/api/routes integration proxies) | `dhis2 route` | 7 tools |  |
| Maintenance (tasks, cache, cleanup, data integrity) | `dhis2 maintenance` | 8 tools | [Maintenance plugin](architecture/maintenance-plugin.md) |
| Dev (codegen, uid, pat, oauth2 client, sample fixtures) | `dhis2 dev` |  | [Codegen](codegen.md) |
| Playwright PAT | `dhis2-browser pat` |  | [PAT helper](pat-helper.md) |

Every MCP tool accepts an optional `profile: str | None` kwarg so an agent can target any configured profile per call.

Day-to-day workflows (`make install`, `make lint`, `make test`, `make docs-serve`) are documented in the repo root `README.md`.
