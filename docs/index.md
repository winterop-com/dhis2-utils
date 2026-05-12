# dhis2w

Python tooling for DHIS2. A `uv` workspace with an async client library, a Typer CLI, a FastMCP server, a Playwright browser helper, a code generator, and a shared plugin runtime.

## Where to start

- **New to the repo?** Skim the [Walkthrough](walkthrough.md), set up [a local DHIS2](local-setup.md), then pick a guide.
- **Writing Python that talks to DHIS2?** Read the [Python library tutorial](guides/client-tutorial.md). Every block is runnable.
- **Using the CLI?** [Connecting to DHIS2](guides/connecting-to-dhis2.md) covers Basic / PAT / OAuth2 setup with profiles.
- **Looking for the architecture?** Start at [Overview](architecture/overview.md), then [Typed schemas](architecture/typed-schemas.md) + [Codegen](codegen.md).
- **Browsing by symbol?** The [API reference](api/index.md) auto-renders every `dhis2w-client` module's docstrings.

## Packages

| Package | Role | PyPI |
| --- | --- | --- |
| `dhis2w‑client` | Async DHIS2 API client with pluggable auth and pydantic models | [`dhis2w‑client`](https://pypi.org/project/dhis2w-client/) |
| `dhis2w‑core` | Profile discovery, plugin registry, first-party plugins | [`dhis2w‑core`](https://pypi.org/project/dhis2w-core/) |
| `dhis2w‑cli` | Typer console script `dhis2` (mounts plugins from `dhis2w-core`) | [`dhis2w‑cli`](https://pypi.org/project/dhis2w-cli/) |
| `dhis2w‑mcp` | FastMCP server `dhis2w-mcp` (mounts the same plugins) | [`dhis2w‑mcp`](https://pypi.org/project/dhis2w-mcp/) |
| `dhis2w‑browser` | Playwright helpers (PAT creation, future UI automation) | [`dhis2w‑browser`](https://pypi.org/project/dhis2w-browser/) |
| `dhis2w‑codegen` | Version-aware client generator | _workspace-only_ |

Plus `infra/`, a docker-compose stack for running a local DHIS2 instance with pre-seeded PATs and an OAuth2 client.

## Capability matrix

337 MCP tools across 13 plugin groups; 16 top-level CLI domains (current as of v0.10.x — auto-regenerated count lives in [`docs/mcp-reference.md`](mcp-reference.md)). Every MCP tool accepts an optional `profile: str | None` kwarg so an agent can target any configured profile per call; every CLI command has a matching MCP tool (and vice versa) sharing one typed service call.

| Domain | CLI | MCP tools | Docs |
| --- | --- | ---: | --- |
| Profile (list / verify / show / default / add / remove / rename, login / logout / bootstrap) | `dhis2 profile` | 4 | [Profiles](architecture/profiles.md) |
| System (whoami, info, server-info, calendar get/set) | `dhis2 system` | 5 | [System module](architecture/system.md) |
| Metadata — core surface (`list` / `get` / `patch` / `search` / `usage` / `export` / `import` / `diff` / `diff-profiles` / `merge`) | `dhis2 metadata` | 230 | [Metadata plugin](architecture/metadata-plugin.md) |
| Metadata — authoring triples (org-units, data-elements, indicators, program-indicators, category-options + legend-sets + options + attribute + program-rule + sql-view + viz + dashboard + map) | `dhis2 metadata <sub-app>` | — (part of metadata count above) | [Organisation units](api/organisation-units.md) / [Data elements](api/data-elements.md) / [Indicators](api/indicators.md) / [Program indicators](api/program-indicators.md) / [Category options](api/category-options.md) / [Legend sets](api/legend-sets.md) |
| Data (aggregate `dataValueSets` + `dataValues`, tracker entities / enrollments / events / relationships / push) | `dhis2 data aggregate` + `dhis2 data tracker` | 15 | [Aggregate plugin](architecture/aggregate.md) / [Tracker plugin](architecture/tracker.md) |
| Analytics (aggregate / event / enrollment / outlier / tracked-entity queries) | `dhis2 analytics` | 5 | [Analytics plugin](architecture/analytics.md) |
| Route (`/api/routes` integration proxies) | `dhis2 route` | 7 | [Auth schemes](api/auth-schemes.md) |
| Maintenance (tasks, cache, cleanup, data integrity, validation, predictors) | `dhis2 maintenance` | 15 | [Maintenance plugin](architecture/maintenance-plugin.md) |
| Files (documents + file resources) | `dhis2 files` | 5 | [Files plugin](architecture/files-plugin.md) |
| Messaging (`/api/messageConversations` + ticket-workflow fields) | `dhis2 messaging` | 11 | [Messaging plugin](architecture/messaging-plugin.md) |
| User admin (users, user-groups, user-roles, sharing) | `dhis2 user` + `dhis2 user-group` + `dhis2 user-role` | 16 | [User plugin](architecture/user-plugin.md) / [User groups + roles](architecture/user-groups-and-roles.md) |
| Customize (login page / logos / CSS / system settings) | `dhis2 dev customize` | 7 | [Customize plugin](architecture/customize-plugin.md) |
| Apps (`/api/apps` + `/api/appHub` + snapshot/restore) | `dhis2 apps` | 13 | [Apps API](api/apps.md) |
| Doctor (BUGS tripwires + integrity checks + metadata health) | `dhis2 doctor` | 4 | [Doctor plugin](architecture/doctor-plugin.md) |
| Dev (codegen, uid, pat, oauth2 client, sample fixtures) | `dhis2 dev` | — (dev-only) | [Codegen](codegen.md) |
| Browser automation (Playwright-driven PAT mint, screenshots, OIDC login) | `dhis2 browser` | — (runs out-of-process) | [Browser automation](architecture/browser.md) |

Day-to-day workflows (`make install`, `make lint`, `make test`, `make docs-serve`) are documented in the repo root `README.md`.
