# Workspace layout

The repo is a `uv` workspace with a virtual root (the root `pyproject.toml` has no `[project]`, only `[tool.uv.workspace]`). Every shippable unit of code is its own member under `packages/`.

## Why a workspace instead of one package

Three reasons:

- **`dhis2w-client` has to be publishable on its own.** A single-package layout would force PyPI users of the client to pull in Typer, FastMCP, Playwright — none of which they need. A workspace lets us ship the client lean.
- **CLI and MCP shouldn't be the same install.** A server running `dhis2w-mcp` in a Docker image doesn't need the CLI's Typer tree. A developer running `dhis2` locally doesn't need the MCP stdio loop. Separate members, separate wheels.
- **New surfaces land cleanly.** A future FastAPI web UI or a TUI is a new folder, not a conditional import inside an existing package.

## Layout

```
dhis2-utils/
├── pyproject.toml                # virtual workspace root + shared tool config
├── uv.lock                       # single workspace-wide lock
├── Makefile                      # drives install/lint/test/docs/build/publish
├── mkdocs.yml                    # docs config (claude theme, left-side nav)
├── CLAUDE.md                     # non-negotiable project rules
├── docs/                         # this site's source
├── site/                         # mkdocs output (gitignored)
├── examples/
└── packages/
    ├── dhis2w-client/             # pure httpx + pydantic lib, PyPI-publishable
    ├── dhis2w-core/               # profile system + plugin runtime + first-party plugins
    ├── dhis2w-cli/                # Typer console script
    ├── dhis2w-mcp/                # FastMCP server
    ├── dhis2w-browser/            # Playwright helpers
    └── dhis2w-codegen/            # generator — registers `dhis2 codegen` subcommand
```

## Configuration split

All lint/type/test tooling (ruff, mypy, pyright, pytest, coverage) is configured **once** at the workspace root. Members inherit these settings automatically — no per-member `ruff.toml` or duplicated mypy stanzas.

Each member's `pyproject.toml` has just:

- `[project]` — name, version, description, Python floor, dependencies
- `[project.scripts]` — console entrypoints (only `dhis2w-cli` and `dhis2w-mcp`)
- `[project.entry-points."dhis2.plugins"]` — plugin registration (for `dhis2w-codegen` and future plugin packages)
- `[build-system]` — `uv_build` backend

## Build + publish

`make build` produces wheels for all members. `make publish-client PUBLISH=1` pushes only `dhis2w-client` to PyPI — the other members stay private.

## Open questions

- **Do we ever publish `dhis2w-codegen` to PyPI?** Probably, once it stabilises. Users of the client library outside this repo would still need a way to generate versioned models for their own instance.
- **Docs per-member or one site?** Currently one site. If per-member doc surfaces grow significantly, we may split to one mkdocs config per member stitched together, but starting unified is simpler.
