# Decisions log

Running list of architectural choices and the reasoning behind them. Each entry is a terse "we decided X because Y, alternatives were Z". This file is a first stop when you're wondering "why is it done that way?".

## 2026-04-17 — uv workspace instead of single package

**Decision:** repo is a virtual `uv` workspace with multiple members under `packages/`.

**Why:** `dhis2-client` must ship to PyPI without dragging Typer/FastMCP/Playwright deps. MCP servers deployed in Docker don't need the CLI. New surfaces (FastAPI, TUI) should land as new folders, not conditional imports.

**Alternatives rejected:**

- Single package with optional-dependency extras — doesn't reduce import-time surface, and extras don't help when users install from PyPI.
- Monorepo with separate PyPI projects per top-level folder — same thing, more ceremony.

## 2026-04-17 — Chapkit's linter config copied verbatim

**Decision:** ruff + mypy + pyright configs in the workspace root match chapkit exactly.

**Why:** chapkit is the house standard. Matching conventions across personal projects means less mental overhead. Divergence requires justification.

## 2026-04-17 — `dhis2-claude-theme` for docs with left-side nav only

**Decision:** mkdocs with the custom claude theme, `navigation.sections` + `navigation.expand` + `navigation.indexes` features, no `navigation.tabs`.

**Why:** user finds top-tab nav distracting. The sidebar carries everything, auto-expanded.

## 2026-04-17 — Plugin runtime in `dhis2-core`, both CLI and MCP mount it

**Decision:** plugins live in `dhis2-core/plugins/<name>/` with `service.py` + `cli.py` + `mcp.py`. `dhis2-cli` and `dhis2-mcp` discover them at startup via module walk + entry points.

**Why:** MCP tool calls should never subprocess the CLI (latency, lost typing, text parsing). Sharing `service.py` across both surfaces gives parity for free and lets tests cover both through one code path.

**Alternatives rejected:**

- MCP shelling out to `dhis2` CLI — slow, brittle, loses pydantic in/out.
- MCP importing Typer commands programmatically — fights Typer's CLI ergonomics; you end up wanting the underlying function anyway.

## 2026-04-17 — Pluggable auth via Protocol

**Decision:** `dhis2-client` defines `AuthProvider` Protocol; ships Basic/PAT/OAuth2 providers; accepts any conforming class.

**Why:** DHIS2 has at least three auth mechanisms in common use (Basic, PAT, OAuth2/OIDC) and future providers will appear (service-account JWT, OIDC federation, proxied auth). Hardcoding auth into the client means forking it whenever a new mechanism is needed.

## 2026-04-17 — OAuth2 loopback via `asyncio.start_server`

**Decision:** OAuth2 provider uses `asyncio.start_server` for the loopback redirect, not `http.server.HTTPServer` on a thread.

**Why:** native async cleanup, no thread-pool juggling, no concurrent-request surprise, clearer lifecycle. Matches the async-first stance of the rest of the client.

**Alternative rejected:** running `http.server.HTTPServer.handle_request` in `run_in_executor`. Works, but requires custom subclass for silent logging and doesn't integrate with async task cancellation.

## 2026-04-17 — Version-aware committed generated clients

**Decision:** `dhis2_client.generated.v{40,41,42,43}/` are separate modules, populated by `dhis2 codegen`, committed to git. `Dhis2Client.connect()` picks the right one via `/api/system/info`.

**Why:** user's explicit direction. DHIS2 schemas evolve per version; a single hand-curated client either lags or grows shims. Committed generated code means PyPI users don't need to run the generator, and diffs are reviewable in PRs.

**Alternatives rejected:**

- Runtime dynamic models (`pydantic.create_model`) — kills static analysis, no autocomplete, pyright-strict incompatible.
- Single hand-written model set covering v40–v43 — combinatorial explosion of optional fields, or worse, silent accuracy drift.
- Code-generated output gitignored and regenerated at CI — PyPI install wouldn't have the types.

## 2026-04-17 — Strict version dispatch by default, opt-in soft fallback

**Decision:** `Dhis2Client` raises `UnsupportedVersionError` when the reported DHIS2 version has no generated module. `allow_version_fallback=True` enables nearest-lower fallback with a warning (never nearest-higher).

**Why:** strict by default protects library users from silently losing typed fields. Agents and CLIs that want to keep running against unknown versions opt in explicitly; library code that cares about correctness gets the default.

## 2026-04-17 — Async-only, no sync façade

**Decision:** all public APIs in `dhis2-client` are `async`. No sync wrapper generated via `unasync` or similar.

**Why:** FastMCP and FastAPI are async, httpx is async, and notebook users who actually need sync can do `asyncio.run(...)`. A sync wrapper would double the test surface for negligible ergonomic gain.

## 2026-04-17 — camelCase fields in generated pydantic models

**Decision:** generated pydantic models use DHIS2's camelCase field names directly (e.g. `displayName`), not snake_case with aliases.

**Why:** eliminates alias translation at parse/serialise time; the wire format and the Python field names are identical. Codegen output is explicitly not PEP 8 pure — it mirrors the source API.

## 2026-04-17 — SQLAlchemy + SQLite for persisted state

**Decision:** any persistent storage in this workspace (OAuth2 tokens, metadata cache, run history) uses SQLAlchemy async + aiosqlite with Alembic migrations. No Postgres, no raw SQL, no pickled files.

**Why:** SQLite is the correct scale for personal/project-scoped tooling. SQLAlchemy gives us typed `Mapped[...]` columns for free. Alembic means schema changes are reviewable.

## 2026-04-17 — Filesystem-scan version discovery, not a hardcoded list

**Decision:** `dhis2_client.generated.available_versions()` walks the `generated/` folder and imports each `v\d+` subpackage, returning only those whose `__init__.py` sets `GENERATED = True`. No hardcoded `_KNOWN` tuple.

**Why:** originally the list was hardcoded to `("v40", "v41", "v42", "v43")`. Play dev turned out to be v44, which broke discovery. Scanning the filesystem means adding a new version is literally just running codegen — no Python edit required.

## 2026-04-17 — Codegen templates use relative imports

**Decision:** generated `__init__.py` does `from .resources import Resources`, and `resources.py` does `from .models.<name> import <Name>`. Not absolute `from dhis2_client.generated.v44.resources ...`.

**Why:** absolute imports tie the generated code to exactly one install location, breaking when the module is imported from tmp_path during tests, or if a downstream project vendors the generated code elsewhere. Relative imports resolve wherever the package sits.

## 2026-04-17 — Codegen derives resource class names from `schema.klass`, not `schema.name`

**Decision:** the Java-class tail (`klass.rsplit(".", 1)[-1]`) is the primary identifier for a generated resource. `schema.singular` and `schema.name` are fallbacks.

**Why:** `schema.name` is not unique across DHIS2's `/api/schemas` response — six schemas (JobConfiguration, Route, etc.) all report `name="identifiableObject"`. `klass` is fully qualified and always distinct. The emitter also dedupes by final class name + plural attr-name to catch any remaining collisions.

## 2026-04-17 — Generated resources return raw dicts for create/update/delete

**Decision:** `create`, `update`, and `delete` return `dict[str, Any]` — the raw DHIS2 import-summary response — not parsed pydantic models.

**Why:** DHIS2's response shape for write operations (`{status, stats, response: {uid, errorReports, ...}}`) is not the resource shape. Parsing into the resource model would discard detail. Typed GET/LIST keep pydantic; write responses stay raw.

## 2026-04-17 — System module is hand-written, not generated

**Decision:** `/api/system/info` and `/api/me` get hand-written `SystemInfo` / `Me` pydantic models in `dhis2_client/system.py`. `client.system.info()` and `client.system.me()` are accessors on the client.

**Why:** these aren't metadata types, so `/api/schemas` doesn't describe them. Hand-writing is correct. Same reasoning will apply to tracker, data values, and analytics — all non-metadata endpoints with their own response shapes.

## 2026-04-17 — Integration tests use string fixtures, not shared dataclass

**Decision:** `conftest.py` in each member exposes `play_url`, `play_username`, `play_password` as separate session-scoped string fixtures. Test files accept them as individual parameters rather than a single `PlayCredentials` object.

**Why:** pytest's conftest auto-discovery doesn't make fixtures importable as module attributes — `from tests.conftest import PlayCredentials` fails in mypy and at runtime (`tests/` is not a real package). Flat string fixtures sidestep that entirely and let each member have its own conftest.

## 2026-04-17 — COMPLEX schema properties become `Any`, not `dict[str, Any]`

**Decision:** codegen maps DHIS2 schema property type `COMPLEX` to `Any` in generated pydantic fields.

**Why:** empirically, DHIS2's COMPLEX fields return dicts, lists, empty lists, or nested arrays of dicts across different metadata types. `dict[str, Any]` forces pydantic to reject anything non-dict, which breaks real server responses (observed with `Constant.attributeValues = []`). `Any` plus `extra="allow"` preserves the payload without validation failures.

## 2026-04-17 — Generated CRUD dumps with `mode="json"`

**Decision:** `create` and `update` in the generated resources template use `model.model_dump(by_alias=True, exclude_none=True, mode="json")`.

**Why:** default pydantic dumps leave `datetime` objects raw, which `httpx.Request(json=...)` cannot serialise. `mode="json"` converts datetime → ISO 8601 strings and handles other JSON-unfriendly types transparently. No cost on models that don't have such fields.

## 2026-04-17 — `DHIS2_HEADFUL=1` env var flips Playwright to visible mode

**Decision:** `dhis2_browser.session.resolve_headless()` is the single source of truth for headed-vs-headless. Explicit `headless=bool` kwargs override. Otherwise, `DHIS2_HEADFUL=1` (or `true`/`yes`/`on`) shows the browser; anything else keeps it headless.

**Why:** tests and automation want headless for speed; humans debugging a flow want to see what's happening. A single env var applied across every Playwright entry point (CLI, test fixtures, programmatic callers) means one switch controls all of them.

## 2026-04-17 — Dep floors bumped to installed latest

**Decision:** every `>=` floor across member and workspace `pyproject.toml` files was raised to match the currently-installed version. Major-version gaps (e.g. `fastmcp>=2.0` while we run 3.x, `pytest>=8.4` while we run 9.x, `mkdocstrings>=0.26` while we run 1.x) were closed.

**Why:** the lockfile always pinned latest — but the floors in pyproject.toml were stale reading "we support 2.x" when we actively require 3.x features. Tightening the floors keeps documentation and constraints honest, without changing actual installed versions. Future `uv lock --upgrade` runs (`make deps-upgrade`) continue to pick up latest.

## 2026-04-17 — Playwright PAT helper uses Playwright for login, API for creation

**Decision:** `dhis2_browser.create_pat` navigates to the DHIS2 login UI with Playwright (driven form fill + submit), then uses the authenticated browser context's `page.request.post` to hit `/api/apiToken`. It does not automate the PAT-creation UI.

**Why:** mixing UI flow (for auth cookie) with API flow (for PAT creation) is robust to future UI changes — the login selectors are stable across DHIS2 versions; the PAT UI isn't. Using the authenticated context's request client preserves cookies without us having to marshal them manually.

## 2026-04-17 — In-process FastMCP Client for MCP testing

**Decision:** MCP integration tests construct a `FastMCP` server via `build_server()`, hand it to `fastmcp.Client(server)`, and call tools inside the same Python process. No subprocess, no stdio framing.

**Why:** FastMCP's `Client` accepts a `FastMCP` instance directly when you pass the server object. This gives real tool invocation through FastMCP's dispatch machinery without the cost or flakiness of spawning a subprocess. ~50ms per test instead of multi-second. The code path exercised is the same one an external agent would hit; we only skip transport serialization.

## 2026-04-17 — CLI tested via `typer.testing.CliRunner`, not subprocess

**Decision:** `dhis2-cli` integration tests use `CliRunner().invoke(build_app(), [...])` rather than `subprocess.run(["uv", "run", "dhis2", ...])`.

**Why:** subprocess invocation is ~2s per test (venv resolution overhead). CliRunner runs Typer dispatch in-process in ~5ms and covers everything that can actually break — command wiring, Typer argument parsing, async-run bridging, printed output. The console-script entry point itself is a one-liner we trust.

## 2026-04-17 — Shared `profile_from_env()` for CLI and MCP

**Decision:** every plugin service call reads the DHIS2 profile from environment variables via `dhis2_core.profile.profile_from_env()`. CLI commands and MCP tools both call this at invocation time; no profile threading through arguments.

**Why:** keeps the two surfaces perfectly symmetric. The CLI user exports env vars in their shell; the MCP client configures `env` in its server spec. Neither surface has to invent its own profile flag. A future `.dhis2/profiles.toml` layer will be added inside `profile_from_env()` without either surface changing.

## 2026-04-17 — Tests auto-source seeded `.env.auth`

**Decision:** conftest files in `dhis2-client`, `dhis2-cli`, and `dhis2-mcp` walk up from the test file to find `infra/home/credentials/.env.auth` and `os.environ.setdefault(...)` every line. Explicit env overrides win; the seeded file is a fallback.

**Why:** when the user runs `make dhis2-up-seeded`, we write the PATs into that file. The test suite picks them up automatically on the next `make test-slow` run — no manual `source` step. The `setdefault` means CI or an explicit env override still takes precedence.

## 2026-04-17 — mypy excludes `conftest.py` to allow per-member conftests

**Decision:** root `pyproject.toml` sets `[tool.mypy] exclude = "^packages/[^/]+/tests/conftest\\.py$"`.

**Why:** two `conftest.py` files at sibling `tests/` dirs both resolve to the module name `conftest`, which mypy rejects as duplicate. Excluding them from mypy is pragmatic — they're fixture-only, pytest still discovers them normally, and actual test functions stay fully typechecked.
