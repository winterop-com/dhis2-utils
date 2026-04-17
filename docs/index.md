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
| `dhis2-cli` | Typer console script `dhis2` | private |
| `dhis2-mcp` | FastMCP server `dhis2-mcp` | private |
| `dhis2-browser` | Playwright helpers | private |
| `dhis2-codegen` | Version-aware client generator | private |

Day-to-day workflows (`make install`, `make lint`, `make test`, `make docs-serve`) are documented in the repo root `README.md`.
