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

Fifteen top-level domains: `analytics`, `browser`, `data`, `dev`, `doctor`, `files`, `maintenance`, `messaging`, `metadata`, `profile`, `route`, `system`, `user`, `user-group`, `user-role`. Plus a nested `dev customize` for rarely-run branding / theming. Each plugin shares a `service.py` between the CLI and MCP sides; the same typed call from both surfaces.

`dhis2 metadata` has the full CRUD surface: `list` / `get` / `patch` (RFC 6902) + bundle `export` / `import` / `diff` (file-vs-file and file-vs-live) with per-resource filter support and an automatic dangling-reference warning on export. Plus workflow-specific sub-apps: `metadata options show / find / sync` for OptionSet sync, `metadata attribute get / set / delete / find` for cross-resource AttributeValue workflows (ICD / SNOMED / external-system-id mapping). `dhis2 doctor` runs ~100 checks on a live instance (20 metadata-health probes + 81 DHIS2 integrity checks + BUGS tripwires).

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

- Auto-generated **CLI reference** (`docs/cli-reference.md`, ~3500 lines from the Typer app) + **MCP reference** (`docs/mcp-reference.md`, 105 tools across 12 groups from the FastMCP server). Both regenerated on every `make docs-build`.
- **Narrative tutorials**: `docs/guides/cli-tutorial.md` (profile setup → patch → export/diff/import → analytics refresh → user admin → doctor), `docs/guides/client-tutorial.md` (profile-based by default; auth + 3-way profile construction up front; every downstream code block uses `open_client(profile_from_env())`).
- **Examples index** (`docs/examples.md`) catalogues 89 runnable examples (45 client, 27 CLI, 17 MCP) with descriptions + cross-links to concept docs. Verified end-to-end against the seeded v42 stack on the last refresh (PR #125).
- **Architecture docs** cover every plugin, the client, auth, profiles, codegen, typed schemas, plugins runtime, external plugins, MCP, versioning, browser automation.
- **`BUGS.md`** — 28 upstream DHIS2 quirks with live `curl` repros + v43 re-audit status.

### Test coverage

498 tests across 80+ files, plus several slow `@pytest.mark.slow` integration tests that exercise live-stack workflows (`--watch` job polling, Playwright PAT creation, Playwright `authenticated_session` + dashboard screenshot capture). Unit + CliRunner + respx-mocked HTTP at `make test`; slow integration tests at `make test-slow` (nightly). `make coverage` runs branch-coverage locally (uses `coverage[toml]` + `pytest-cov`; XML output for tooling consumption) but CI doesn't gate on it yet — see "Near-term plan" below.

Test gaps:

- Property-based tests for `generate_uid` distribution (beyond the existing smoke test).
- Multi-version CI integration tests — v42 only today; v40/41/43/44 codegen is committed but never exercised against a live stack.

### Upstream quirks tracked

28 entries in the repo-root `BUGS.md`. Covers analytics URL-suffix oddities, OAuth2 config cliff, soft-delete semantics, `uid` vs `id` wire-format divergence, login-app layout bug at non-100% zoom, OAS discriminator gaps, attribute-value filter idiosyncrasies, per-resource option DELETE no-op, and the validationResults fields-preset quirk. Re-audited against v43 (2.43.1-SNAPSHOT) when the OAS codegen shipped: none of the OAS-level bugs (#13, #14, #15) are fixed upstream yet — our local workarounds still apply cleanly.

## Gaps surfaced during use

### OIDC / OAuth2 polish

- Token refresh is tested in code but undocumented for end users.
- `Local OIDC` login-page button is non-functional for browser clicks (CLI-only `redirect_url`); no per-provider "hide from login UI" flag in DHIS2 v42 — documented in `docs/architecture/auth.md`.
- Bearer-to-JSESSIONID path for browser workflows on OIDC profiles is unverified (flagged in `authenticated_session` docstring). Smoke-test when the first OIDC-profile browser workflow actually runs.

### Refresh ritual is manual

The "regenerate seeded dump + re-verify every example" cycle landed as PR #125, but each step was a separate shell invocation. A `make refresh-and-verify` target that chains the whole thing (wipe stack → build dump → refresh `.env.auth` → run every example in every surface → summarise) would turn a 30-minute ritual into one command. See Near-term plan #4.

## Near-term plan (next 3–5 PRs)

Ordered by value-per-effort, roughly:

1. **`CHANGELOG.md` + annotated git tags + first PyPI release of `dhis2-client`** — bump the workspace on every merge, tag the PyPI-publishable releases. Scaffolding for eventual public distribution of the pure client. `make publish-client` exists but has never been exercised.
2. **CI coverage gate** — wire `make coverage` into `.github/workflows/ci.yml` and upload `coverage.xml` as an artifact. Optional follow-up: Codecov PR-comment delta (requires a repo token). `pytest-cov` + `coverage[toml]` are already dev deps; `[tool.coverage.run/report]` is configured.
3. **Predictor seed + workflow fixture** — the validation plugin ships with 3 seeded rules + guaranteed violations (PR #111). The predictor side is still bare: `client.predictors` runs expressions but nothing in the seed fixture exercises it end-to-end. Small follow-up that seeds 1–2 predictors (e.g. "3-month rolling average of OPD") + a `PredictorGroup` so `dhis2 maintenance predictors run --group ...` has a concrete target on fresh dumps.
4. **`make refresh-and-verify` target** — one-shot chain of `dhis2-build-e2e-dump` + `dhis2-seed` + example-runner + summary. Would turn PR #125's ad-hoc verification into a repeatable workflow + give CI something to run nightly if we decide to promote it.

BUGS.md #15 (undiscriminated `JobConfiguration.jobParameters` + `WebMessage.response` unions) isn't on the near-term list: the sibling-field discriminator pattern doesn't fit the AuthScheme-style spec-patches approach, and the scheduler plugin isn't an active workflow. Revisit when someone hits a real-world need.

## Strategic options (pick one before the next cycle)

Six independent directions — the right order depends on where the pain is. Each would be a multi-PR body of work.

### 1. Release engineering (lowest-risk, ships soonest)

`CHANGELOG.md` + annotated git tags + first PyPI release of `dhis2-client` + coverage gate on CI. Good hygiene, unblocks public distribution. Small PRs, visible progress.

### 2. Visualizations / dashboards / maps plugin

The largest unclaimed DHIS2 surface without a dedicated plugin. Generic CRUD already works (`dhis2 metadata list visualizations / dashboards / maps`), but workflow-level ergonomics don't:

- `dhis2 viz create --type PIVOT_TABLE --de <uid> --periods LAST_12_MONTHS --ou <uid>` — one-command pivot-table creation from flags instead of a hand-built JSON bundle.
- `dhis2 viz clone <uid> --new-name X` — very common admin flow.
- `dhis2 viz preview <uid> --out foo.png` — render a visualization to PNG via the analytics API + Pillow (server-side; no browser needed for static charts).
- `dhis2 dashboard add-item <dashboard> <viz>` — patch one item into a dashboard without round-tripping the whole thing.
- `dhis2 map layers list <uid>` — map-specific surface.

Big PR set; unlocks automated-reporting use cases (weekly PDF of every dashboard, thumbnail generation, dashboard layout tooling).

### 3. SQL views plugin

`/api/sqlViews` is a powerful admin surface that's not wrapped. Four workflow commands cover the 80%:

- `dhis2 sqlview list` — catalog existing views + their type (VIEW / MATERIALIZED_VIEW / QUERY).
- `dhis2 sqlview execute <uid>` — run the view, return rows as JSON or CSV.
- `dhis2 sqlview create <name> <sql-file>` — create a view from a `.sql` file on disk.
- `dhis2 sqlview refresh <uid>` — kick the materialised-view refresh job.

Typed `SqlViewRow` + `SqlViewExecution` models; respx-mocked unit tests plus a slow integration test that seeds + executes a tiny view against the live stack.

### 4. Program rules workflow

`ProgramRule` + `ProgramRuleVariable` + `ProgramRuleAction` are the tracker-side business-logic surface. Today CRUD works via generic metadata, but there's no workflow surface:

- `dhis2 metadata program-rule list [--program UID]` — all rules in a program + their priority, condition, effect.
- `dhis2 metadata program-rule validate <uid>` — parse-check the rule's condition expression (same shape as the validation-rule expression workflow).
- `dhis2 metadata program-rule trace <program> <event-json>` — dry-run: given an event payload, show which rules would fire in what order. Invaluable for debugging stuck tracker workflows.
- `dhis2 metadata program-rule vars-for <program>` — list every variable in scope for a program's rules.

MCP tools mirror the CLI. Typed input/output models throughout.

### 5. Data approval workflow plugin

`/api/dataApprovals` + `/api/dataApprovalLevels` + `/api/dataApprovalWorkflows` cover multi-level aggregate approval (district → zone → ministry sign-off). Common in humanitarian + government reporting pipelines. Surface:

- `dhis2 dataapproval status <ds> <pe> <ou>` — which level is this cell at? `APPROVED_HERE / APPROVED_ABOVE / UNAPPROVED_READY / UNAPPROVED_WAITING`.
- `dhis2 dataapproval approve / unapprove / accept / unaccept` — the four write verbs.
- `dhis2 dataapproval bulk-status <ds> <pe>` — every org unit for one dataset-period, exit-on-incomplete mode for CI.
- Typed `DataApprovalStatus` enum + level-aware state machine.

### 6. Audit log reader

DHIS2's `/api/audits/*` endpoints track every write by user / timestamp / entity-uid (for DE values, tracker payloads, metadata changes). No wrapper today; integrations that need a "who changed X and when" history have to hand-build URLs.

- `dhis2 audit data-values --de <uid> [--ou <uid>] [--pe <pe>]` — stream every change for a cell.
- `dhis2 audit metadata --klass DataElement --uid <uid>` — metadata edit history for one resource.
- `dhis2 audit tracker-entity <uid>` — tracker write audit.
- `client.audit.iter_data_values(...)` / `iter_metadata(...)` async iterators for library callers.

Niche but valuable for compliance + forensics use cases.

## Medium-term

- **Multi-version CI matrix** — integration tests run against v42 only. Stand up v40 / v41 / v43 / v44 nightly jobs against compose-managed stacks so codegen drift gets caught before release.
- **Metadata-import conflict renderer** — currently `WebMessageResponse.conflicts()` surfaces raw DHIS2 messages; a Rich-table renderer (object UID → offending property → server message) would make `dhis2 metadata import` errors readable in the terminal.
- **Property-based testing on filter / order DSL parsing.**
- **`dhis2 apps` plugin (API-based, not browser).** `GET /api/appHub` lists 100+ hub apps with versions + download URLs; `POST /api/appHub/{versionId}` installs one by version UUID; `GET /api/apps`, `POST /api/apps` (file upload), `DELETE /api/apps/{app}` handle the installed set. First-class plugin under `dhis2-core/plugins/apps/` with `list-hub / install / list / remove` subcommands. Pure HTTP workflow — no Chromium.
- **Org-unit group sets / dimensions plugin** — `/api/organisationUnitGroupSets`, analytics dimensions. Niche but common in analytics configs.

## Long-term / exploratory

- **Further `dhis2-browser` workflows**, layered on `authenticated_session`: **dashboard creation / layout editing** (REST `/api/dashboards` is replace-only; drag-drop layout is UI-only), **Maintenance app driving** (actions that don't have REST), **Org-unit-tree drag-drop edits**. Each deferred until a concrete need appears.
- **Scheduled jobs plugin (`/api/jobConfigurations`).** Blocked on BUGS.md #15 (undiscriminated `jobParameters` + `WebMessage.response` unions). Revisit when the OAS discriminator is fixed upstream, or when a concrete scheduling workflow forces us to hand-roll typed payloads for the common job types.
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
