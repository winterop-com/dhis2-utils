# dhis2-utils

Private DHIS2 tooling — a `uv` workspace containing a pure client library, a Typer CLI, a FastMCP server, a Playwright browser-automation helper, and a shared plugin runtime.

## Workspace members

| Package | Purpose | PyPI |
| --- | --- | --- |
| `dhis2-client` | Pure async httpx + pydantic DHIS2 client with pluggable auth (Basic, PAT, OAuth2/OIDC). Typed models from both `/api/schemas` and `/api/openapi.json` codegen. | publishable |
| `dhis2-codegen` | Generator that emits pydantic models + `StrEnum`s + CRUD accessors into `dhis2_client.generated.v{N}/`. Two source-of-truth paths: `/api/schemas` for metadata resources, `/api/openapi.json` for instance-side shapes (tracker writes, envelopes, auth schemes). | private |
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

## Connecting to a DHIS2 instance

See [`docs/guides/connecting-to-dhis2.md`](docs/guides/connecting-to-dhis2.md) for the full end-to-end walkthrough covering Basic, PAT, and OAuth2/OIDC — including the `dhis.conf` keys the OAuth2 path needs on the DHIS2 server, manual OAuth2 client registration without the seed script, the `openId` user field, and a troubleshooting matrix of every failure mode.

Hard requirements, conventions, and the plugin / auth / workspace model are documented in `CLAUDE.md` and the `docs/` site.
