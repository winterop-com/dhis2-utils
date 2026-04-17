# dhis2-utils

Private DHIS2 tooling — a `uv` workspace containing a pure client library, a Typer CLI, a FastMCP server, a Playwright browser-automation helper, and a shared plugin runtime.

## Workspace members

| Package | Purpose | PyPI |
| --- | --- | --- |
| `dhis2-client` | Pure async httpx + pydantic DHIS2 client with pluggable auth (Basic, PAT, OAuth2/OIDC). | publishable |
| `dhis2-core` | Shared runtime: profile discovery, plugin registry, auth factory, token store, first-party plugins. | private |
| `dhis2-cli` | Typer console script `dhis2`. | private |
| `dhis2-mcp` | FastMCP server `dhis2-mcp`. | private |
| `dhis2-browser` | Playwright helpers for screenshots and future UI automation. | private |

## Quick start

```bash
make install      # sync workspace deps
make lint         # ruff + mypy + pyright
make test         # pytest across all members
make docs-serve   # local mkdocs-material
```

Hard requirements, conventions, and the plugin / auth / workspace model are documented in `CLAUDE.md` and the `docs/` site.
