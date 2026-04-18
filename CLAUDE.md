# CLAUDE.md

Guidance for Claude Code working in this repository.

## NO EMOJIS EVER

Not in commit messages, PR titles, PR descriptions, code comments, docstrings, documentation, design notes, or any output. Use plain text (`[x]`, `[ ]`, `CRITICAL`, `Note:`, `WARNING:`) instead.

## Hard requirements (non-negotiable)

These reshape every decision. Re-read them when in doubt.

1. **Multi-instance support via profiles.** Auto-discover a profile from the current working directory by walking up for `.dhis2/profiles.toml`; fall back to `~/.config/dhis2/profiles.toml`. When nothing is found, CLI runs an interactive setup and MCP tools return an actionable error pointing at `dhis2 init`.
2. **DHIS2 v42+ only.** No compatibility shims for older versions. The client asserts `systemInfo.version >= 2.42` on first call and caches the result.
3. **Auth is pluggable; ship three kinds of provider: Basic, PAT, OAuth2/OIDC.** `dhis2-client` defines an `AuthProvider` Protocol. The client never touches auth internals. OAuth2 uses the OAuth 2.1 authorization-code flow with PKCE against `/oauth2/authorize` and `/oauth2/token`. Future providers (service-account JWT, OIDC federation, proxy-injected headers) land as new files in `dhis2-client/auth/` without touching the client.
4. **Playwright UI automation is isolated in `dhis2-browser`.** API-only installs must not pull Chromium. The screenshot plugin is the first consumer; future UI-update plugins layer on the same helpers.
5. **`uv` for everything Python, organized as a `uv` workspace.** Five members under `packages/`: `dhis2-client`, `dhis2-core`, `dhis2-cli`, `dhis2-mcp`, `dhis2-browser`. Single `uv.lock` at the workspace root, `uv_build` backend. Every member uses the `src/` layout. Shared code lives in a workspace member (never a floating `src/` outside a package). **Never edit `pyproject.toml` deps by hand — use `uv add` / `uv add --dev`.**
6. **FastAPI for any HTTP service, FastMCP for any MCP service.** No Flask, no bare `http.server`, no hand-rolled stdio loops.
7. **Pydantic for ALL structured data. No `dict`s. No `@dataclass`es.** Every type that carries domain meaning — DHIS2 resources, service return values, CLI output shapes, MCP tool returns, error bodies, configuration, view-models, command options — is a `pydantic.BaseModel`. DHIS2 resource models (Me, SystemInfo, DataElement, Indicator, …) live in `dhis2-client/models/` so PyPI users of the client get them. Plugin-internal view-models (reports, job state, summaries) live in the plugin's `models.py`. `Dhis2Client` returns parsed models, not raw dicts.

    - `dict[str, Any]` is allowed only at the HTTP/JSON boundary (the raw response body inside `_parse_json` before it's validated) and for pass-through escape hatches like `get_raw` / `post_raw` whose callers immediately wrap the result in a model.
    - `@dataclass` is not allowed — even for "internal" types. If it needs named fields, it's a `BaseModel`. Use `model_config = ConfigDict(frozen=True)` when you'd have reached for `@dataclass(frozen=True)`.
    - Tuples-as-structs (`(name, code, description)`) are not allowed in new code — name the fields in a model.
    - CLI commands still accept Typer parameters, but anything the command produces (JSON output, table rows, return values consumed by another layer) is a model, not a `dict`.
8. **pytest for ALL testing.** `pytest-asyncio` (auto), `respx` for HTTP mocking, `typer.testing.CliRunner` for CLI, in-process `httpx.AsyncClient` for FastMCP/FastAPI integration tests. No `unittest`.
9. **ruff + mypy + pyright for ALL Python code**, strict configs. Copied verbatim from `/Users/morteoh/dev/chap-sdk/chapkit/pyproject.toml`. All three must pass under `make lint`.
10. **If any persistent storage is needed, default to SQLAlchemy + SQLite over asyncio** — `sqlalchemy[asyncio]` with `aiosqlite`, typed `Mapped[...]` columns, Alembic for migrations. DB files live beside the active profile (`.dhis2/tokens.sqlite`, `.dhis2/cache.sqlite`). No Postgres, no ORM-free raw SQL, no pickled files.
11. **Typer for every CLI** — root CLI, plugin sub-apps, anything in `examples/`. No `argparse`, no `click` directly, no `sys.argv` parsing.
12. **CLI surface is heavily preferred.** New capabilities expose a CLI command first and an MCP tool second, both calling the same `service.py`. Plugins without a `cli.py` need explicit justification; plugins without an `mcp.py` are fine (e.g. `profile` is CLI-only).
13. **Makefile drives every workflow.** `make install / lint / test / test-slow / coverage / docs / docs-serve / docs-build / migrate / upgrade / downgrade / build / publish-client / clean`. CI calls make targets, not raw commands.
14. **Docs use mkdocs-material.** `mkdocs.yml` mirrors chapkit's. Docs live in `docs/`; build output in `site/` (gitignored). API reference uses `mkdocstrings` to auto-generate from pydantic models and service docstrings.

## Architecture

Three orthogonal axes of extension — extending one never forces edits to another:

- **Workspace members** (`packages/`): each shippable unit. New surfaces (a future FastAPI web UI, another SDK) land as new members.
- **Plugins** (`dhis2-core/plugins/<name>/`): each DHIS2 domain is a folder with `__init__.py`, `models.py`, `service.py`, `cli.py`, `mcp.py`, `tests/`. Discovered automatically by iterating `dhis2_core.plugins.*`; external plugins register via `importlib.metadata.entry_points(group="dhis2.plugins")`.
- **Auth providers** (`dhis2-client/auth/`): `AuthProvider` Protocol. Ship Basic, PAT, OAuth2. Add more without touching `client.py`.

Dependency arrows (no cycles):

```
dhis2-browser ─► dhis2-client
dhis2-core    ─► dhis2-client
dhis2-cli     ─► dhis2-core  (─► dhis2-browser as optional extra)
dhis2-mcp     ─► dhis2-core  (─► dhis2-browser as optional extra)
```

## Documentation standards

- Every Python file: one-line module docstring at top.
- Every class: one-line docstring.
- Every method/function: one-line docstring.
- Format: triple quotes `"""docstring"""`. Google style. Keep it one line when possible.

## Keep docs and examples in sync with code

Every behaviour-changing PR must leave `docs/` and `examples/` matching the new reality. Not later — **in the same PR**.

- Rename a kwarg, add a flag, change a return type, rename a directory? Grep for the old name across `docs/`, `examples/`, `README.md`, top-level architecture pages, and every `*.md` in `docs/guides/`. Update each hit or record an explicit reason not to.
- Add a new plugin command or MCP tool? Add an example under `examples/cli/` and `examples/mcp/` (plus `examples/client/` if the new surface has a library path).
- Add a new make target or script? Mention it in the target's help line + in whichever page under `docs/` documents the nearest neighbour.
- Remove a feature or rename a package? Sweep the same places — stale references that point at removed code are worse than no docs.
- Run `make docs-build` after doc edits so broken links surface.

If a change legitimately doesn't need a doc or example update, say so in the PR description so the reviewer doesn't have to reconstruct that reasoning.

## Git workflow

Branch + PR is the default. Ask before creating branches or PRs.

- Branch naming: `feat/*`, `fix/*`, `refactor/*`, `docs/*`, `test/*`, `chore/*`
- Commit prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`
- NEVER include "Co-Authored-By: Claude" or any AI attribution.
- NEVER use emojis in commits, PR titles, or PR descriptions.
- Always run `make lint && make test` before opening a PR.

## Naming

Full descriptive names, no abbreviations. `repository` not `repo`. `profile_store` not `ps`. Applies to classes, attributes, locals, parameters.

## Code quality

- Python 3.13+, line length 120, type annotations required everywhere.
- Double quotes. `async/await` throughout the runtime. Conventional commits.
- Class order: public → protected → private.
- `__all__` only in `__init__.py` files when exporting a package surface.
- Always run `make lint` and `make test` after changes.

## Dependency management

```
uv add <package>             # runtime dep, in the right member
uv add --dev <package>       # dev dep (workspace root)
uv add --package <member> <package>   # add to a specific workspace member
uv lock --upgrade            # refresh the workspace lock
```

**Never edit `pyproject.toml` deps by hand.**
