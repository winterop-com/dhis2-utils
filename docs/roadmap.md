# Roadmap

A running inventory of what the workspace covers today, gaps surfaced during use, and the near-term plan. Pre-1.0, no deployed users; every item is a judgment call about priority, not a commitment.

## Current state

### Workspace surface

| Package | Role |
| --- | --- |
| `dhis2-client` | Async HTTP client, pluggable auth, typed responses via generated models. Retry policy, task awaiter, connection-pool tuning all first-class. |
| `dhis2-codegen` | `/api/schemas` → pydantic emitter + OAS spec-patches framework (synthesises Jackson discriminators upstream DHIS2 omits) |
| `dhis2-core` | Plugin runtime + shared services (profiles, CLI errors, task watch, client context) |
| `dhis2-cli` | Typer root that discovers every plugin (first-party + entry-point) |
| `dhis2-mcp` | FastMCP server that mounts the same plugins |
| `dhis2-browser` | Playwright session helpers (auth through the DHIS2 login form) |

### CLI surface

Fourteen top-level domains: `analytics`, `data`, `dev`, `doctor`, `files`, `maintenance`, `messaging`, `metadata`, `profile`, `route`, `system`, `user`, `user-group`, `user-role`. Plus a nested `dev customize` for rarely-run branding / theming. Each plugin shares a `service.py` between the CLI and MCP sides; the same typed call from both surfaces.

`dhis2 metadata` has the full CRUD surface: `list` / `get` / `patch` (RFC 6902) + bundle `export` / `import` / `diff` (file-vs-file and file-vs-live) with per-resource filter support and an automatic dangling-reference warning on export. `dhis2 doctor` runs ~100 checks on a live instance (20 metadata-health probes + 81 DHIS2 integrity checks + BUGS tripwires).

### Typed models shipped

Via `/api/schemas` codegen (`generated/v{40,41,42,43,44}/schemas/`):

- 100+ metadata resources (DataElement, DataSet, OrganisationUnit, Indicator, Program, …) with full CRUD accessors including the RFC 6902 `patch(uid, ops)` method
- 77+ `StrEnum`s for CONSTANT properties (ValueType, AggregationType, DataElementDomain, …)
- A shared `Reference` with both `id` and `code` fields

Via `/api/openapi.json` codegen (`generated/v{N}/oas/`, currently populated on v42 + v43):

- Every `components/schemas` entry — 562 classes + 260 StrEnums + 104 aliases on v42; 984 classes on v43.
- Consumers in `dhis2-client`: `envelopes.py`, `auth_schemes.py`, `aggregate.py`, `system.py`, `maintenance.py`, and `generated/v42/tracker.py` are all thin shims over the OAS output.
- Emitter is deterministic + version-scoped; `dhis2 dev codegen oas-rebuild --version v{N}` regenerates from the committed `openapi.json` without network.
- **Spec-patches framework** for known-upstream OAS gaps (`dhis2_codegen.spec_patches`). Each patch is idempotent + carries a `bugs_ref` pointer; the rebuild log names which gap was worked around. Current patches: `*AuthScheme` discriminators (BUGS.md #14 — still unfixed in v43).

Remaining hand-written in `dhis2-client` (by design):

- `WebMessageResponse` subclass + `DataIntegrityReport` / `DataIntegrityResult` / `Me` / `Notification` — helper methods and client-side convenience shapes that aren't in OpenAPI.
- `AnalyticsMetaData` — typed parser helper over `Grid.metaData` (a bare `dict[str, Any]` on the wire). `Grid` / `GridHeader` come straight from the OAS codegen.
- `TrackerBundle` — the `POST /api/tracker` envelope isn't in OpenAPI under that name. Thin wrapper on OAS tracker models.
- `PeriodType` (24 canonical period names, class-hierarchy upstream so not emitted by either codegen path).

### Typing posture

The four-PR typing sweep (#71-#74) plus the codegen discriminator synthesis (#76) eliminated every `dict[str, Any]` signature that crosses module boundaries outside the explicit HTTP-boundary carveouts. Every service-layer function returns a typed pydantic model; MCP tools dump at the edge via `_dump_model`; CLI handlers dump for JSON output or Rich tables. The CLAUDE.md "no dict[str, Any] across module boundaries" rule is enforced workspace-wide.

### Runtime features

- `--profile/-p` global override + `~/.config/dhis2/profiles.toml` or `./.dhis2/profiles.toml` auto-discovery
- `--debug/-d` global flag → stderr HTTP trace lines via `dhis2_client.http` logger
- `--watch/-w` on job-kicking commands (`analytics refresh`, `maintenance dataintegrity run`) + standalone `maintenance task watch` with Rich progress UI
- `--json` opt-in on every write command; concise one-line summary by default
- Typed `Dhis2ApiError.web_message` parses the envelope on 4xx so the CLI surfaces `conflicts[]` / `importCount` / `rejectedIndexes[]` detail
- Client-side UID generation (`generate_uid`, `generate_uids`); no `/api/system/id` round-trip
- External plugin loading via `importlib.metadata.entry_points(group="dhis2.plugins")` — see `examples/plugin-external/` for a minimal runnable reference
- **Retry policy** with exponential backoff + jitter + `Retry-After` header honouring. Idempotent-only by default; opt in for POST/PATCH per policy. Threads through `Dhis2Client(retry_policy=...)` and `open_client(profile, retry_policy=...)`.
- **Library-level task awaiter** — `client.tasks.await_completion(task_ref)` blocks until DHIS2 reports `completed=True`; `iter_notifications` for streaming renderers. Reuses the already-open HTTP connection (no new handshake per poll).
- **Connection-pool tuning** — `Dhis2Client(http_limits=httpx.Limits(...))` / `open_client(profile, http_limits=...)` for sizing against the real DHIS2 capacity.
- **Data-integrity streaming iterator** — `client.maintenance.iter_integrity_issues(...)` yields `IntegrityIssueRow`s (issue + owning check's name / displayName / severity) as a flat stream. Caller walks every issue with `async for`, filters or groups with one-liners, breaks mid-stream without building the full list.
- **Files plugin** — `dhis2 files documents {list,get,upload,upload-url,download,delete}` + `dhis2 files resources {upload,get,download}`. `client.files` accessor with typed `Document` / `FileResource` models. Binary document upload automatically uses the two-step fileResource+link workflow DHIS2 forces on callers (see BUGS.md #16).
- **System metadata cache** — TTL-bounded per-client in-memory cache on `client.system` for `info()` / `default_category_combo_uid()` / `setting(key)`. 300 s default TTL; primed on `connect()` so the first `info()` after connect is free. `invalidate_cache(key=...)` for selective drops. Tune via `system_cache_ttl=...` on `Dhis2Client` / `open_client`; pass `None` to disable.
- **Bulk delete on `client.metadata`** — `client.metadata.delete_bulk(resource_type, [uid, ...])` + `delete_bulk_multi({resource: [uids], ...})` wrap `POST /api/metadata?importStrategy=DELETE` as a single request. Empty UID lists short-circuit without an HTTP call. Partial-failure behaviour tunable via `atomic_mode` (`NONE` default; `ALL` rolls back on any conflict). Returns a `WebMessageResponse` whose `.import_report().stats.deleted` carries the count.
- **Streaming data-value-set import** — `client.data_values.stream(source, content_type=...)` feeds httpx's chunked transfer directly from a `Path`, `bytes`, sync / async iterable, or async generator. Never buffers the body in Python memory. Supports JSON / XML / CSV / ADX; forwards every standard `/api/dataValueSets` knob (`dry_run`, `import_strategy`, id-schemes, `skip_audit`, `async_job`). Returns a `WebMessageResponse` with the typed `ImportCount`.
- **Multi-instance metadata diff** — `dhis2 metadata diff-profiles <a> <b> -r <resource>` (+ MCP `metadata_diff_profiles`) exports the same slice from two registered profiles concurrently and diffs them structurally. Required per-resource scoping + per-resource `--filter resource:prop:op:val` + extensible `--ignore` list keep noise (timestamps, sharing, translations) out of the drift count. `--exit-on-drift` for the CI shape.

### CI + release engineering

- `.github/workflows/ci.yml` runs `make lint && make test && make docs-build` on every PR
- `.github/workflows/e2e.yml` nightly — full DHIS2 stack + seeded fixtures + slow integration tests
- No `CHANGELOG.md` yet; no git tags
- `make publish-client` exists but hasn't been exercised

### Docs

- Auto-generated **CLI reference** (`docs/cli-reference.md`, ~3200 lines from the Typer app) + **MCP reference** (`docs/mcp-reference.md`, 78 tools across 11 groups from the FastMCP server). Both regenerated on every `make docs-build`.
- **Narrative tutorials**: `docs/guides/cli-tutorial.md` (profile setup → patch → export/diff/import → analytics refresh → user admin → doctor), `docs/guides/client-tutorial.md` (profile-based by default; auth + 3-way profile construction up front; every downstream code block uses `open_client(profile_from_env())`).
- **Examples index** (`docs/examples.md`) catalogues 85+ runnable examples (42 client, 25 CLI, 18 MCP) with descriptions + cross-links to concept docs.
- **Architecture docs** cover every plugin, the client, auth, profiles, codegen, typed schemas, plugins runtime, external plugins, MCP, versioning.
- **`BUGS.md`** — 25 upstream DHIS2 quirks with live `curl` repros + v43 re-audit status.

### Test coverage

446 tests across 80 files, plus 3 slow `@pytest.mark.slow` integration tests that exercise `--watch` end-to-end against the live DHIS2 stack. Unit + CliRunner + respx-mocked HTTP at `make test`; slow integration tests at `make test-slow` (nightly). `make coverage` runs branch-coverage locally (uses `coverage[toml]` + `pytest-cov`; XML output for tooling consumption) but CI doesn't gate on it yet — see "Near-term plan" below. Gaps:

- Property-based tests for `generate_uid` distribution (beyond the existing smoke test)
- No tests for `dhis2-browser`'s login-form flow (Playwright isolation keeps it out of `make test`)

### Upstream quirks tracked

25 entries in the repo-root `BUGS.md`. Covers analytics URL-suffix oddities, OAuth2 config cliff, soft-delete semantics, `uid` vs `id` wire-format divergence, login-app layout bug at non-100% zoom, OAS discriminator gaps, etc. Re-audited against v43 (2.43.1-SNAPSHOT): none of the OAS-level bugs (#13, #14, #15) are fixed upstream yet — our local workarounds still apply cleanly.

## Gaps surfaced during use

### `dhis2-browser` has one user and no follow-on

The screenshot plugin was the initial consumer. No UI-automation examples for the commonly-asked workflows (e.g. scripted dashboard creation, imports/exports through the web UI when the API path is blocked). Potential future surface.

### OIDC / OAuth2 polish

- Token refresh is tested in code but undocumented for end users
- `Local OIDC` login-page button is non-functional for browser clicks (CLI-only `redirect_url`); no per-provider "hide from login UI" flag in DHIS2 v42 — documented in `docs/architecture/auth.md`

## Near-term plan (next 3–5 PRs)

Ordered by value-per-effort, roughly:

1. **`CHANGELOG.md` + annotated git tags + first PyPI release** — bump the workspace on every merge, tag the PyPI-publishable `dhis2-client` releases. Scaffolding for eventual public distribution of `dhis2-client`.
2. **CI coverage gate** — wire `make coverage` into `.github/workflows/ci.yml` and upload `coverage.xml` as an artifact. Optional follow-up: Codecov PR-comment delta (requires a repo token). `pytest-cov` + `coverage[toml]` are already dev deps; `[tool.coverage.run/report]` is configured.
3. **Sweep remaining raw-client callsites in examples + infra** — the service-layer `get_raw`/`post_raw` calls are all wrapped in `Model.model_validate(raw)` on the next line (Bucket B carveout), but ~30 `examples/client/*` and `infra/scripts/*` raw calls could be upgraded to typed accessors on a case-by-case basis. Low-urgency follow-up to the typing sweep (#71-#74, #76).

BUGS.md #15 (undiscriminated `JobConfiguration.jobParameters` + `WebMessage.response` unions) isn't on the near-term list: the sibling-field discriminator pattern doesn't fit the AuthScheme-style spec-patches approach, and the scheduler plugin isn't an active workflow. Revisit when someone hits a real-world need.

## Strategic options (pick one before the next cycle)

Three fundamentally different directions for the next cycle. Each independently good; the right order depends on where the pain is.

### 1. Release engineering (lowest-risk, ships soonest)

`CHANGELOG.md` + annotated git tags + first PyPI release of `dhis2-client` + coverage gate on CI. Good hygiene, unblocks public distribution. Small PRs, visible progress.

### 2. New DHIS2 surface: expand plugin coverage

Thirteen top-level domains today. Large adjacent surfaces with no dedicated plugin:

| Surface | Value | Shape | Recommend as… |
| --- | --- | --- | --- |
| **visualizations / dashboards / maps** | Medium-high; needed for UI-adjacent automation | Large surface (Visualization, Map, Dashboard, pivot tables, favourite sharing) | **Top recommendation now**; bigger PR. Unlocks automated reporting scripts. |
| **org-unit group sets / dimensions** | Low-medium; niche but common in analytics configs | `/api/organisationUnitGroupSets`, dimensions | Low urgency. |
| **scheduled jobs (`/api/jobConfigurations`)** | Low-medium; blocked on BUGS.md #15 for typed `jobParameters` | Job list / enable-disable / trigger / history | Revisit when the OAS discriminator is fixed upstream. |

### 3. Remaining library polish

- **Raw-client callsite sweep in examples + infra** — ~30 `examples/client/*` + `infra/scripts/*` files still use `get_raw` / `post_raw` where a typed accessor (or `client.metadata.save_bulk` / `client.analytics.stream_to`) would be cleaner. Low-urgency mechanical upgrade.

## Medium-term

- Property-based testing on filter/order DSL parsing

## Long-term / exploratory

- **`Notification` enum typing**: OpenAPI ships typed `category` / `dataType` / `level` enums. Wiring them would give enum autocomplete on `await_task` / `client.tasks.await_completion` callbacks, at the cost of threading new imports through every caller. Incremental improvement; do when the next maintenance-plugin touch lands.
- **Browser-only workflows** as first-class plugins: scripted dashboard composition, visualization creation, org-unit-tree edits; anything currently only reachable through the DHIS2 web UI. Each as a `dhis2-browser` subcommand.
- **`dhis2-codegen` as a standalone PyPI package** once the emitter stabilises; lets external projects target their own DHIS2 schema. Both `/api/schemas` and OAS paths are plumbed through the same CLI now.

## Reference: dhis2-java-client

Apache-2.0 Java client maintained by the DHIS2 org ([dhis2/dhis2-java-client](https://github.com/dhis2/dhis2-java-client)). Targeted comparison against this workspace as of this writing:

### Already covered here

- Typed `/api/sharing` — `Sharing`, `SharingBuilder`, `ACCESS_*` constants, `apply_sharing` / `get_sharing` helpers. Full parity with the Java client's sharing builder; used throughout the examples.
- User administration — `dhis2 user list / get / me / invite / reinvite / reset-password`. User-group + user-role plugins covering membership + authority-bundle flows.
- Branding / theming — `dhis2 dev customize logo-front/banner/style/set/apply/show` + `Dhis2Client.customize` accessor. Covers `/api/staticContent/*`, `/api/files/style`, `/api/systemSettings/*`. No equivalent in the Java client.
- Auth providers (Basic, PAT, OAuth2); ours is async-first with a typed `AuthProvider` Protocol, theirs is blocking HttpClient-based.
- Generated resource CRUD across v40/v41/v42/v43/v44 (Java is hand-maintained).
- WebMessageResponse envelope parsing; we expose `.import_count()`, `.conflicts()`, `.rejected_indexes()`, `.task_ref()`, `.created_uid()`.
- Full metadata query surface; repeatable `--filter`, `--order`, `rootJunction=AND|OR`, `--page`/`--page-size`, `--all`, `--translate`/`--locale`, every `fields` selector form.
- **Metadata bundle export / import / diff + RFC 6902 patch** (beyond Java parity): `dhis2 metadata export` + `import` + `diff` + `patch` with per-resource filters + dangling-reference warning on export.
- Paging; `list_raw(..., paging=True)` returns the pager; `list(..., paging=False)` walks the full catalog.
- Typed filter values on enum fields; `ValueType.NUMBER` is a `StrEnum`, substitutable into filter strings directly.
- Client-side UID generation; matches the Java `CodeGenerator` algorithm exactly.
- Typed tracker writes; `TrackerBundle` + `TrackerTrackedEntity` / `TrackerEnrollment` / `TrackerEvent` models for `POST /api/tracker`.
- Event + enrollment analytics; outlier detection + tracked-entity analytics.

### Considered, not adopted

- **Fluent query builder (`.addFilter(Filter.eq("name", "ANC"))`)**: the Java client wraps DHIS2's `property:operator:value` string syntax in a chainable builder. Deliberately skipped — Python f-strings make `f"name:like:{name}"` already readable; the builder doesn't buy type safety on the stringly-typed value side; DHIS2's own docs teach the string form.

### Worth evaluating later (Java parity)

- **Domain-specific response types beyond `WebMessageResponse`**: Java has distinct `PagedResponse`, `Stats`, `Response` for different endpoint shapes. We collapse into `WebMessageResponse` + helpers. The OAS codegen already emits the specific shapes (`TrackerImportReport`, `ImportReport`, etc.) — swap on-demand when a specific call site hits friction.

### Beyond Java parity (already shipped)

Items that don't exist in the Java client and now exist here:

- **Retry / backoff** — `RetryPolicy` on `Dhis2Client` + `open_client` with exponential backoff, jitter, `Retry-After` honoured, idempotent-only by default.
- **Library-level task awaiter** — `client.tasks.await_completion(task_ref, ...)` + `client.tasks.iter_notifications(...)` for streaming renderers.
- **Connection-pool tuning** — `http_limits` kwarg on `Dhis2Client` and `open_client`.
- **Typed codegen** across five DHIS2 versions via schema-driven emission; Java is hand-maintained.
- **OAS spec-patches framework** — synthesises the Jackson discriminators DHIS2's OpenAPI generator omits (`Route.auth` et al.), so generated models are cleanly typed without upstream action.
- **Data-integrity streaming iterator** — `client.maintenance.iter_integrity_issues()` yields a flat stream of `IntegrityIssueRow`s tagged with owning-check metadata.
- **System metadata cache** — TTL-bounded in-memory cache on `client.system` for `info()` / `default_category_combo_uid()` / `setting(key)`. Primed on `connect()` so the first `info()` call is free.
- **Bulk metadata delete** — `client.metadata.delete_bulk(resource_type, uids)` + `delete_bulk_multi({...})` wrap `/api/metadata?importStrategy=DELETE`.
- **Typed bulk-save on every generated resource** — `client.resources.<resource>.save_bulk(items)` accepts `list[TypedModel | dict]` and POSTs as a `/api/metadata` bundle. Shipped on all 77 DHIS2 resource types in one codegen template change. Supports `import_strategy` + `atomic_mode` + `dry_run`.
- **`client.metadata.dry_run(by_resource)`** — cross-resource `importMode=VALIDATE` entry point. Accepts typed models or dicts; runs DHIS2's full preheat + validation pipeline without committing.
- **Streaming analytics export** — `client.analytics.stream_to(destination, *, params, endpoint="/api/analytics.json")` pipes httpx's chunked response straight to disk via `aiter_bytes`. Counterpart to `client.data_values.stream` (import). Handles JSON / CSV / XLSX / rawData.json / events+enrollments query endpoints — any `/api/analytics*` path. Repeated-key params (`{"dimension": [...]}` or `list[tuple]`) land as multiple query params. Returns bytes written; raises `Dhis2ApiError` / `AuthenticationError` on 4xx/401 without writing a partial file.
- **Messaging plugin** — `dhis2 messaging {list,get,send,reply,mark-read,mark-unread,delete}` + `messaging_*` MCP tools + `client.messaging` accessor. Typed `MessageConversation` from the OAS schema. Pairs with the files plugin: upload `MESSAGE_ATTACHMENT`-domain fileResources via `client.files` and reference them from `send` / `reply`. Papers over BUGS.md #17 (DHIS2 returns the new conversation UID on the `Location` header instead of in the envelope) by parsing the header + GET-ing back a typed conversation.
- **Validation + predictors workflow** — `dhis2 maintenance validation {run,result,validate-expression,send-notifications}` + `dhis2 maintenance predictors run` (+ `maintenance_validation_*` / `maintenance_predictors_run` MCP tools + `client.validation` / `client.predictors` accessors). Runs validation-rule analyses, browses persisted `ValidationResult` rows, parse-checks expressions against DHIS2's per-context parsers, and triggers predictor expressions. CRUD on rules / predictors themselves stays on the generic metadata surface.
- **Streaming dataValueSets import** — `client.data_values.stream(source, content_type=...)` feeds httpx's chunked transfer directly (`Path` / `bytes` / sync / async iter).
- **Multi-instance metadata diff** — `dhis2 metadata diff-profiles` exports two profiles concurrently + diffs them with per-resource filters + extensible `--ignore`.
- **Files plugin** — CLI + MCP + `client.files` accessor over `/api/documents` + `/api/fileResources` with typed `Document` / `FileResource` models + two-step binary upload (workaround for BUGS.md #16).
- **Interactive CLI pickers** — `dhis2 profile default` (no arg) launches an arrow-key menu via `questionary`; keyboard-driven in-TUI picks over registered profiles.

### Beyond Java parity (not yet)

(Empty — major Java-parity gaps are closed.)

## Explicit non-goals

- Python < 3.13. New typing features (StrEnum, TypeAliasType, PEP 604 unions, PEP 695 generics) justify the bump.
- DHIS2 < v42. Every backport fork splits the code; no deployed users so no reason.
- Flask / argparse / raw stdio MCP loops / hand-rolled TOML parsers; every slot has a chosen standard per the CLAUDE.md hard-requirements list in the repo root.
- A second filter DSL layered on top of DHIS2's `property:operator:value` string syntax. See the dhis2-java-client comparison above for the rationale.
- Synchronous client variant. `async` throughout is a hard requirement.
- `dict[str, Any]` crossing module boundaries. CLAUDE.md hard rule; enforced workspace-wide as of the typing sweep (#71-#74, #76). New code that proposes dict-in-signature needs explicit justification referencing a specific HTTP-boundary carveout.

## How this file gets updated

Greenfield voice; edits describe the current state of the plan, not its history. When a near-term item ships, delete it from the "near-term" list (don't rewrite to "already shipped"). Use the PR's own description for the history; this file is always about what's next.
