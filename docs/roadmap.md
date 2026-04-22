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

Fifteen top-level domains: `analytics`, `browser`, `data`, `dev`, `doctor`, `files`, `maintenance`, `messaging`, `metadata`, `profile`, `route`, `system`, `user`, `user-group`, `user-role`. Each plugin shares a `service.py` between the CLI and MCP sides; the same typed call from both surfaces.

`dhis2 metadata` has the full workflow surface:

- **Core CRUD**: `list` / `get` / `patch` (RFC 6902).
- **Cross-resource search**: `dhis2 metadata search <query>` — fans out three concurrent `/api/metadata?filter=<field>:ilike:<q>` calls (`id`, `code`, `name`) and merges by UID. Full UID, partial UID, business code, or name fragment all flow through one verb.
- **Bundle operations**: `export` / `import` / `diff` (file-vs-file and file-vs-live) with per-resource filters + dangling-reference warning on export; `diff-profiles` for staging-vs-prod drift.
- **Authoring sub-apps**: `options show / find / sync` for OptionSet sync; `attribute get / set / delete / find` for cross-resource AttributeValue workflows; `program-rule show / vars-for / validate-expression / where-de-is-used`; `sql-view list / show / execute / refresh / adhoc`; `viz list / show / create / clone / delete`; `dashboard list / show / add-item / remove-item`; `map list / show / create / clone / delete`.

`dhis2 doctor` runs ~100 checks on a live instance (20 metadata-health probes + 81 DHIS2 integrity checks + BUGS tripwires).

### MCP surface

126 tools across 12 plugin groups (`analytics_*`, `customize_*`, `data_*`, `dev_*`, `doctor_*`, `files_*`, `maintenance_*`, `messaging_*`, `metadata_*`, `profile_*`, `system_*`, `user_*`). Every CLI command has an MCP tool equivalent and vice versa; both share one typed service call.

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
- `PeriodType` + `RelativePeriod` StrEnums (24 period frequencies + 45 rolling windows; upstream Java enums the OpenAPI schema doesn't expose — see BUGS.md #28).

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
- **Library-level task awaiter** — `client.tasks.await_completion(task_ref)` blocks until DHIS2 reports `completed=True`; `iter_notifications` for streaming renderers.
- **Connection-pool tuning** — `Dhis2Client(http_limits=httpx.Limits(...))` / `open_client(profile, http_limits=...)` for sizing against the real DHIS2 capacity.
- **Data-integrity streaming iterator** — `client.maintenance.iter_integrity_issues(...)` yields `IntegrityIssueRow`s (issue + owning check's name / displayName / severity) as a flat stream.
- **Files plugin** — `dhis2 files documents {list,get,upload,upload-url,download,delete}` + `dhis2 files resources {upload,get,download}`.
- **System metadata cache** — TTL-bounded per-client in-memory cache on `client.system` for `info()` / `default_category_combo_uid()` / `setting(key)`. 300 s default TTL.
- **Bulk delete on `client.metadata`** — `delete_bulk(resource_type, [uids])` + `delete_bulk_multi({...})` wrap `POST /api/metadata?importStrategy=DELETE`.
- **`client.metadata.search`** — cross-resource UID / code / name search; three concurrent `/api/metadata?filter=<field>:ilike:<q>` calls merged client-side with UID dedup. Typed `SearchResults(query, hits: {resource: [SearchHit, ...]}, total)`.
- **`client.visualizations`** — `VisualizationSpec` typed builder (chart type, data elements, indicators, periods, relative periods, legend set, placement overrides) + `create_from_spec / clone / list / delete` accessor. `RelativePeriod` StrEnum covers the 45 rolling windows upstream OpenAPI exposes as boolean flags.
- **`client.maps`** — `MapSpec` + `MapLayerSpec` typed builder with `indicators`, `legend_set`, thematic / boundary / facility layer kinds; parallels the viz accessor.
- **`client.dashboards`** — `DashboardSlot` + `add_item` / `remove_item` on the dashboards accessor, no round-trip of the whole dashboard.
- **Streaming data-value-set import** — `client.data_values.stream(source, content_type=...)` feeds httpx's chunked transfer directly from a `Path`, `bytes`, sync / async iterable, or async generator. JSON / XML / CSV / ADX.
- **Streaming analytics export** — `client.analytics.stream_to(destination, *, params, endpoint="/api/analytics.json")` pipes httpx's chunked response straight to disk via `aiter_bytes`.
- **Multi-instance metadata diff** — `dhis2 metadata diff-profiles <a> <b> -r <resource>` exports two registered profiles concurrently and diffs them structurally.

### Seed fixture

The committed e2e dump (`infra/dhis-v42.sql.gz`) mirrors DHIS2 Play's Sierra Leone immunization demo: 1332 org units with GeoJSON geometries, 67 data elements, 3 indicators, 2 programs (Child Programme + Antenatal), 2 datasets, 3 dashboards, 23 visualizations built programmatically via `VisualizationSpec`, 8 maps built via `MapSpec`, 188k aggregate data values, 500 tracker entities, 6 program rules + 10 program indicators. `make refresh-and-verify` wipes the stack, rebuilds the dump, runs every non-interactive example, and reports a pass/fail summary — 91 examples pass, 15 skipped (need synthesized fixtures the play snapshot doesn't ship), 0 fail on the current main.

### CI

- `.github/workflows/ci.yml` runs `make lint && make test && make docs-build` on every PR
- `.github/workflows/e2e.yml` nightly — full DHIS2 stack + seeded fixtures + slow integration tests

Public distribution (PyPI, tagged releases, `CHANGELOG.md`) is explicitly out of scope — this workspace is internal-only.

### Docs

- Auto-generated **CLI reference** (`docs/cli-reference.md`, ~3700 lines from the Typer app) + **MCP reference** (`docs/mcp-reference.md`, 126 tools across 12 groups from the FastMCP server). Both regenerated on every `make docs-build`.
- **Narrative tutorials**: `docs/guides/cli-tutorial.md`, `docs/guides/client-tutorial.md`, `docs/guides/visualizations.md` (step-by-step viz + dashboard composition).
- **Examples index** (`docs/examples.md`) catalogues 107 runnable examples (56 client, 33 CLI, 18 MCP) with descriptions + cross-links to concept docs.
- **Architecture docs** cover every plugin, the client, auth, profiles, codegen, typed schemas, plugins runtime, external plugins, MCP, versioning, browser automation.
- **`BUGS.md`** — 29 upstream DHIS2 quirks with live `curl` repros + v43 re-audit status.

### Test coverage

617 tests run via `make test` (648 collected including 31 slow-marked for the nightly integration stack). Unit + CliRunner + respx-mocked HTTP. Slow tests exercise live-stack workflows (`--watch` job polling, Playwright PAT creation, dashboard screenshot capture). `make coverage` runs branch-coverage locally but CI doesn't gate on it yet.

Test gaps:

- Property-based tests for `generate_uid` distribution (beyond the existing smoke test).
- Multi-version CI integration tests — v42 only today; v40/41/43/44 codegen is committed but never exercised against a live stack.

### Upstream quirks tracked

29 entries in the repo-root `BUGS.md`, up from 22 at the start of the viz / seed cycle. The last seven landed while reforming the seed: DataSet Hibernate flush ordering (#23), Person-TET built-in name collisions (#24), `/api/.../metadata` leaking computed fields (#25), admin OU scope cached per session (#26), fresh-install flakiness on first metadata import (#27), `RelativePeriods` OAS schema shape (#28), and `/api/metadata` ignoring `rootJunction` (#29 — the reason `metadata search` has to fan out N requests instead of one).

## Gaps surfaced during use

### OIDC / OAuth2 polish

- Token refresh is tested in code but undocumented for end users.
- `Local OIDC` login-page button is non-functional for browser clicks (CLI-only `redirect_url`); no per-provider "hide from login UI" flag in DHIS2 v42 — documented in `docs/architecture/auth.md`.
- Bearer-to-JSESSIONID path for browser workflows on OIDC profiles is unverified (flagged in `authenticated_session` docstring).

### Seed fixture narrows some examples

Eight `examples/` (SQL views, SNOMED_CODE attributes, `VACCINE_TYPE` option set, outlier detection) expected synthesized Norway-only fixtures that the play42 immunization snapshot doesn't ship. `verify_examples.py` skip-lists them today — either augment `infra/fixtures/play/` with the missing resource shapes, or rewrite those examples to auto-discover what's on the instance. Counts as tech debt rather than a feature gap.

## Near-term plan (next 3–5 PRs)

Ordered by value-per-effort, roughly:

1. **CI coverage gate** — wire `make coverage` into `.github/workflows/ci.yml` and upload `coverage.xml` as an artifact. `pytest-cov` + `coverage[toml]` are already dev deps; `[tool.coverage.run/report]` is configured.
2. **Predictor seed + workflow fixture** — the validation plugin ships with 3 seeded rules + guaranteed violations (PR #111). The predictor side is still bare: `client.predictors` runs expressions but nothing in the seed fixture exercises it end-to-end. Seed 1–2 predictors (e.g. "3-month rolling average of immunization doses") + a `PredictorGroup` so `dhis2 maintenance predictors run --group ...` has a concrete target on fresh dumps.
3. **Bulk metadata patch on the client** — complements `delete_bulk`. `client.metadata.patch_bulk(resource, [(uid, ops), ...])` runs a list of RFC 6902 patches in one request, returns `WebMessageResponse` with per-UID status. Useful for mass value-type fixes, sharing rollout, etc.
4. **Seed SQL view + Attribute fixture** — augment `infra/fixtures/play/` with one SQL view, one Attribute with DE/option bindings, and a `VACCINE_TYPE`-style option set so the 8 currently-skipped examples (SQL views, attribute workflows, options) unskip.

BUGS.md #15 (undiscriminated `JobConfiguration.jobParameters` + `WebMessage.response` unions) isn't on the near-term list: the sibling-field discriminator pattern doesn't fit the AuthScheme-style spec-patches approach, and the scheduler plugin isn't an active workflow. Revisit when someone hits a real-world need.

## Strategic options (pick one before the next cycle)

Three independent directions — the right order depends on where the pain is. Each would be a multi-PR body of work.

### 1. Data approval workflow plugin

`/api/dataApprovals` + `/api/dataApprovalLevels` + `/api/dataApprovalWorkflows` cover multi-level aggregate approval (district → zone → ministry sign-off). Common in humanitarian + government reporting pipelines. Surface:

- `dhis2 dataapproval status <ds> <pe> <ou>` — which level is this cell at? `APPROVED_HERE / APPROVED_ABOVE / UNAPPROVED_READY / UNAPPROVED_WAITING`.
- `dhis2 dataapproval approve / unapprove / accept / unaccept` — the four write verbs.
- `dhis2 dataapproval bulk-status <ds> <pe>` — every org unit for one dataset-period, exit-on-incomplete mode for CI.
- Typed `DataApprovalStatus` enum + level-aware state machine.

### 2. Audit log reader

DHIS2's `/api/audits/*` endpoints track every write by user / timestamp / entity-uid (for DE values, tracker payloads, metadata changes). No wrapper today; integrations that need a "who changed X and when" history have to hand-build URLs.

- `dhis2 audit data-values --de <uid> [--ou <uid>] [--pe <pe>]` — stream every change for a cell.
- `dhis2 audit metadata --klass DataElement --uid <uid>` — metadata edit history for one resource.
- `dhis2 audit tracker-entity <uid>` — tracker write audit.
- `client.audit.iter_data_values(...)` / `iter_metadata(...)` async iterators for library callers.

Niche but valuable for compliance + forensics use cases.

### 3. Tracker authoring workflows

Generic tracker CRUD works today, but everyday operator flows aren't first-class:

- `dhis2 tracker register <program> --attrs ...` — register + enroll a tracked entity in one verb.
- `dhis2 tracker enroll <te> <program> --at <ou>` — enroll an existing TE without rewriting it.
- `dhis2 tracker event add <enrollment> --stage <uid> --data-values ...` — create one event on a known stage.
- `dhis2 tracker outstanding <program>` — list open enrollments missing required stages (due-date analytics).

Fills a surface the MCP agent side could use heavily; complements the Child Programme + Antenatal programs now in the seed.

## Medium-term

- **`dhis2 apps` plugin (API-based, not browser)** — `GET /api/appHub` lists 100+ hub apps with versions + download URLs; `POST /api/appHub/{versionId}` installs one by version UUID; `GET /api/apps`, `POST /api/apps` (file upload), `DELETE /api/apps/{app}` handle the installed set. First-class plugin under `dhis2-core/plugins/apps/` with `list-hub / install / list / remove` subcommands. Pure HTTP workflow — no Chromium.
- **Multi-version CI matrix** — integration tests run against v42 only. Stand up v40 / v41 / v43 / v44 nightly jobs against compose-managed stacks so codegen drift gets caught before release.
- **Metadata-import conflict renderer** — currently `WebMessageResponse.conflicts()` surfaces raw DHIS2 messages; a Rich-table renderer (object UID → offending property → server message) would make `dhis2 metadata import` errors readable in the terminal.
- **Property-based testing on filter / order DSL parsing.**
- **Org-unit group sets / dimensions plugin** — `/api/organisationUnitGroupSets`, analytics dimensions. Niche but common in analytics configs.

## Long-term / exploratory

- **Further `dhis2-browser` workflows**, layered on `authenticated_session`: Maintenance app driving (actions that don't have REST), Org-unit-tree drag-drop edits. Dashboard creation is covered by the REST `DashboardsAccessor.add_item`; layout drag-drop is UI-only but deferred until a concrete need appears.
- **Scheduled jobs plugin (`/api/jobConfigurations`)** — blocked on BUGS.md #15 (undiscriminated `jobParameters` + `WebMessage.response` unions). Revisit when the OAS discriminator is fixed upstream, or when a concrete scheduling workflow forces us to hand-roll typed payloads for the common job types.
- **Interactive aggregate-data-entry TUI** — `dhis2 data entry <ds> <pe> <ou>` launches a terminal spreadsheet bound to one data set × period × org unit. Questionary or textual for the UI; posts via `client.data_values.stream` on save. Powerful offline-capable data-entry fallback when the UI is down.

## Reference: dhis2-java-client

Apache-2.0 Java client maintained by the DHIS2 org ([dhis2/dhis2-java-client](https://github.com/dhis2/dhis2-java-client)). Targeted comparison against this workspace as of this writing:

### Already covered here

- Typed `/api/sharing` — `Sharing`, `SharingBuilder`, `ACCESS_*` constants, `apply_sharing` / `get_sharing` helpers. Full parity with the Java client's sharing builder.
- User administration — `dhis2 user list / get / me / invite / reinvite / reset-password`. User-group + user-role plugins covering membership + authority-bundle flows.
- Branding / theming — `dhis2 dev customize logo-front/banner/style/set/apply/show` + `Dhis2Client.customize` accessor. No equivalent in the Java client.
- Auth providers (Basic, PAT, OAuth2); ours is async-first with a typed `AuthProvider` Protocol.
- Generated resource CRUD across v40/v41/v42/v43/v44 (Java is hand-maintained).
- WebMessageResponse envelope parsing; `.import_count()`, `.conflicts()`, `.rejected_indexes()`, `.task_ref()`, `.created_uid()`.
- Full metadata query surface; repeatable `--filter`, `--order`, `rootJunction=AND|OR`, `--page`/`--page-size`, `--all`, `--translate`/`--locale`, every `fields` selector form.
- Metadata bundle export / import / diff + RFC 6902 patch with per-resource filters + dangling-reference warning on export.
- Paging; `list_raw(..., paging=True)` returns the pager; `list(..., paging=False)` walks the full catalog.
- Typed filter values on enum fields; `ValueType.NUMBER` is a `StrEnum`, substitutable into filter strings directly.
- Client-side UID generation; matches the Java `CodeGenerator` algorithm exactly.
- Typed tracker writes; `TrackerBundle` + `TrackerTrackedEntity` / `TrackerEnrollment` / `TrackerEvent` models for `POST /api/tracker`.
- Event + enrollment analytics; outlier detection + tracked-entity analytics.

### Considered, not adopted

- **Fluent query builder (`.addFilter(Filter.eq("name", "Penta"))`)**: the Java client wraps DHIS2's `property:operator:value` string syntax in a chainable builder. Deliberately skipped — Python f-strings make `f"name:like:{name}"` already readable; the builder doesn't buy type safety on the stringly-typed value side; DHIS2's own docs teach the string form.

### Worth evaluating later (Java parity)

- **Domain-specific response types beyond `WebMessageResponse`**: Java has distinct `PagedResponse`, `Stats`, `Response` for different endpoint shapes. We collapse into `WebMessageResponse` + helpers. The OAS codegen already emits the specific shapes (`TrackerImportReport`, `ImportReport`, etc.) — swap on-demand when a specific call site hits friction.

### Beyond Java parity (already shipped)

Items that don't exist in the Java client and now exist here:

- **Retry / backoff** — `RetryPolicy` on `Dhis2Client` + `open_client` with exponential backoff, jitter, `Retry-After` honoured, idempotent-only by default.
- **Library-level task awaiter** — `client.tasks.await_completion(task_ref, ...)` + `client.tasks.iter_notifications(...)`.
- **Connection-pool tuning** — `http_limits` kwarg on `Dhis2Client` and `open_client`.
- **Typed codegen** across five DHIS2 versions via schema-driven emission; Java is hand-maintained.
- **OAS spec-patches framework** — synthesises the Jackson discriminators DHIS2's OpenAPI generator omits (`Route.auth` et al.).
- **Data-integrity streaming iterator** — `client.maintenance.iter_integrity_issues()` yields a flat stream of `IntegrityIssueRow`s tagged with owning-check metadata.
- **System metadata cache** — TTL-bounded in-memory cache on `client.system` for `info()` / `default_category_combo_uid()` / `setting(key)`.
- **Bulk metadata delete** — `client.metadata.delete_bulk(resource_type, uids)` + `delete_bulk_multi({...})`.
- **Cross-resource metadata search** — `client.metadata.search(query)` returns typed `SearchResults` grouped by resource; handles UID / partial UID / code / name in one verb.
- **Typed Visualization + Map + Dashboard builders** — `VisualizationSpec`, `MapSpec` + `MapLayerSpec`, `DashboardSlot`. Chart-type-aware dimension placement, typed data dimensions (DEs + indicators), `RelativePeriod` enum for rolling windows, legend-set support. CLI + MCP surfaces on top.
- **Per-viz + per-dashboard PNG capture** — `dhis2 browser viz screenshot` + `dhis2 browser dashboard screenshot` + `dhis2 browser map screenshot`, Chromium-driven via Playwright session helpers.
- **Typed bulk-save on every generated resource** — `client.resources.<resource>.save_bulk(items)`. Supports `import_strategy` + `atomic_mode` + `dry_run`.
- **`client.metadata.dry_run(by_resource)`** — cross-resource `importMode=VALIDATE` entry point.
- **Streaming analytics export** — `client.analytics.stream_to(destination, *, params, endpoint="/api/analytics.json")`.
- **Messaging plugin** — `dhis2 messaging {list,get,send,reply,mark-read,mark-unread,delete}` + `messaging_*` MCP tools + `client.messaging` accessor.
- **Validation + predictors workflow** — `dhis2 maintenance validation {run,result,validate-expression,send-notifications}` + `dhis2 maintenance predictors run`.
- **Streaming dataValueSets import** — `client.data_values.stream(source, content_type=...)`.
- **Multi-instance metadata diff** — `dhis2 metadata diff-profiles` exports two profiles concurrently + diffs them.
- **Files plugin** — CLI + MCP + `client.files` accessor over `/api/documents` + `/api/fileResources`.
- **SQL views runner** — `client.sql_views` + `dhis2 metadata sql-view {list, show, execute, refresh, adhoc}`.
- **Interactive CLI pickers** — `dhis2 profile default` launches an arrow-key menu via `questionary`.

### Beyond Java parity (not yet)

(Empty — major Java-parity gaps are closed.)

## Explicit non-goals

- Python < 3.13. New typing features (StrEnum, TypeAliasType, PEP 604 unions, PEP 695 generics) justify the bump.
- DHIS2 < v42. Every backport fork splits the code; no deployed users so no reason.
- Flask / argparse / raw stdio MCP loops / hand-rolled TOML parsers; every slot has a chosen standard per the CLAUDE.md hard-requirements list in the repo root.
- A second filter DSL layered on top of DHIS2's `property:operator:value` string syntax. See the dhis2-java-client comparison above for the rationale.
- Synchronous client variant. `async` throughout is a hard requirement.
- `dict[str, Any]` crossing module boundaries. CLAUDE.md hard rule; enforced workspace-wide as of the typing sweep (#71-#74, #76). New code that proposes dict-in-signature needs explicit justification referencing a specific HTTP-boundary carveout.
- Public distribution — no PyPI, no tagged releases, no `CHANGELOG.md`. Workspace stays internal.
- `dhis2 program-rule trace` / rule simulator — explicitly declined.

## How this file gets updated

Greenfield voice; edits describe the current state of the plan, not its history. When a near-term item ships, delete it from the "near-term" list (don't rewrite to "already shipped"). Use the PR's own description for the history; this file is always about what's next.
