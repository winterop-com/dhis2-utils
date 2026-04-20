# Roadmap

A running inventory of what the workspace covers today, gaps surfaced during use, and the near-term plan. Pre-1.0, no deployed users; every item is a judgment call about priority, not a commitment.

## Current state

### Workspace surface

| Package | Role |
| --- | --- |
| `dhis2-client` | Async HTTP client, pluggable auth, typed responses via generated models |
| `dhis2-codegen` | `/api/schemas` → pydantic emitter + OAS spec-patches framework |
| `dhis2-core` | Plugin runtime + shared services (profiles, CLI errors, task watch, client context) |
| `dhis2-cli` | Typer root that discovers every plugin (first-party + entry-point) |
| `dhis2-mcp` | FastMCP server that mounts the same plugins |
| `dhis2-browser` | Playwright session helpers (auth through the DHIS2 login form) |

### CLI surface

Eleven top-level domains: `analytics`, `data`, `dev`, `doctor`, `maintenance`, `metadata`, `profile`, `route`, `system`, `user`, `user-group`, `user-role`. Plus a nested `dev customize` for rarely-run branding / theming. Each plugin shares a `service.py` between the CLI and MCP sides; the same typed call from both surfaces.

`dhis2 metadata` has the full CRUD surface including bundle `export` / `import` / `diff` (file-vs-file and file-vs-live) with per-resource filter support and an automatic dangling-reference warning on export. `dhis2 doctor` runs ~95 checks on a live instance (14 metadata-health probes + 81 DHIS2 integrity checks + BUGS tripwires).

### Typed models shipped

Via `/api/schemas` codegen (`generated/v{40,41,42,44}/schemas/`):

- 100+ metadata resources (DataElement, DataSet, OrganisationUnit, Indicator, Program, …) with full CRUD accessors
- 77+ `StrEnum`s for CONSTANT properties (ValueType, AggregationType, DataElementDomain, …)
- A shared `Reference` with both `id` and `code` fields

Via `/api/openapi.json` codegen (`generated/v{N}/oas/`):

- Every `components/schemas` entry — 562 classes + 260 StrEnums + 104 aliases on v42. Covers the instance-side shapes `/api/schemas` can't describe.
- Consumers in `dhis2-client`: `envelopes.py`, `auth_schemes.py`, `aggregate.py`, `system.py`, `maintenance.py`, and `generated/v42/tracker.py` are all thin shims over the OAS output.
- Emitter is deterministic + version-scoped; `dhis2 dev codegen oas-rebuild --version v{N}` regenerates from the committed `openapi.json` without network.
- **Spec-patches framework** for known-upstream OAS gaps (`dhis2_codegen.spec_patches`). Each patch is idempotent + carries a `bugs_ref` pointer; the rebuild log names which gap was worked around. Current patches: `*AuthScheme` discriminators (BUGS.md #14).

Remaining hand-written in `dhis2-client` (by design):

- `WebMessageResponse` subclass + `DataIntegrityReport` / `DataIntegrityResult` / `Me` / `Notification` — helper methods and client-side convenience shapes that aren't in OpenAPI (or where the OpenAPI typing would force invasive caller updates).
- `AnalyticsResponse` + `AnalyticsHeader` + `AnalyticsMetaData` — OpenAPI ships a differently-shaped `Grid` / `GridHeader` / `GridResponse`; migrating forces a behaviour change on every analytics caller. Future cleanup.
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
- External plugin loading via `importlib.metadata.entry_points(group="dhis2.plugins")` — see `examples/plugin-external/` for a minimal runnable reference.

### CI + release engineering

- `.github/workflows/ci.yml` runs `make lint && make test && make docs-build` on every PR
- `.github/workflows/e2e.yml` nightly — full DHIS2 stack + seeded fixtures + slow integration tests
- No `CHANGELOG.md` yet; no git tags
- `make publish-client` exists but hasn't been exercised

### Upstream quirks tracked

22 entries in the repo-root `BUGS.md`. Covers analytics URL-suffix oddities, OAuth2 config cliff, soft-delete semantics, `uid` vs `id` wire-format divergence, login-app layout bug at non-100% zoom, OAS discriminator gaps, etc. Each has a live `curl` repro + "how to know it's fixed" marker.

### Test coverage

67 test files. Unit + CliRunner + respx-mocked HTTP at `make test`; slow integration tests at `make test-slow` (nightly). Gaps:

- Property-based tests for `generate_uid` distribution (beyond the existing smoke test)
- Integration tests that exercise `--watch` end-to-end against the live DHIS2 stack (currently only unit-mocked)
- No tests for `dhis2-browser`'s login-form flow (Playwright isolation keeps it out of `make test`)

## Gaps surfaced during use

### No typed `/api/dataIntegrity/issues` iterator

`dataintegrity result --details` returns the full `DataIntegrityReport` as a typed pydantic model. Large integrity runs (1000s of issues) would benefit from a streaming iterator (`client.maintenance.iter_integrity_issues(...)`) that yields one issue at a time.

### `dhis2-browser` has one user and no follow-on

The screenshot plugin was the initial consumer. No UI-automation examples for the commonly-asked workflows (e.g. scripted dashboard creation, imports/exports through the web UI when the API path is blocked). Potential future surface.

### OIDC / OAuth2 polish

- Token refresh is tested in code but undocumented for end users
- `Local OIDC` login-page button is non-functional for browser clicks (CLI-only `redirect_url`); no per-provider "hide from login UI" flag in DHIS2 v42 — documented in `docs/architecture/auth.md`

### File / document upload surfaces

The `customize` plugin is deliberately scoped to branding. Two adjacent DHIS2 file surfaces are not covered:

- `/api/documents` — user-uploaded attachments (content management).
- `/api/fileResources` — typed files attached to metadata / data capture (data-element images, event photos, etc).

Both are different problem domains — separate plugins when a concrete workflow needs them.

### Concurrent / bulk patterns

No example showing `asyncio.gather` against the client, no guidance on connection-pool sizing for batch workflows.

### No retry / backoff on the client

`Dhis2Client` has no HTTP retry logic — transient 5xx or connection resets fail on the first attempt. `httpx` exposes the hooks cleanly; a typed `RetryPolicy(max_attempts, base_delay)` on the client with sensible defaults would cost ~30 LOC and remove a real failure mode for batch workflows.

### Library-level task awaiter

`--watch` is CLI-only (`dhis2-core/task_watcher.py`). A `client.tasks.await_completion(task_ref, *, timeout, poll_interval)` helper would let library callers block on analytics refreshes / metadata imports / data integrity runs without reaching into the plugin layer.

## Strategic options (pick one before the next cycle)

Three fundamentally different ways to spend the next cycle's work. Each independently good; the right order depends on where the pain is.

### 1. Release engineering + polish (default — lowest risk)

The `CHANGELOG.md` + git tags work unblocks a public `dhis2-client` release on PyPI. Small PRs, visible progress, good hygiene. Default when there's no strategic pressure.

### 2. New DHIS2 surface: expand plugin coverage

Currently covered: `analytics`, `data`, `dev`, `doctor`, `maintenance`, `metadata`, `profile`, `route`, `system`, `user`, `user-group`, `user-role`, plus nested `dev customize` for branding. Large adjacent domains with no dedicated plugin:

| Surface | Value | Shape | Recommend as… |
| --- | --- | --- | --- |
| **validation rules / predictors** | Medium; formulas over data elements | `/api/validationRules`, `/api/predictors`, run/results | **Top recommendation now**; OAS codegen already emits the models, wiring is service + CLI. Completes the data-quality story next to `doctor`. |
| **visualizations / dashboards / maps** | Medium-high; needed for UI-adjacent automation | Large surface (Visualization, Map, Dashboard, pivot tables, favourite sharing) | Strong second; bigger PR. Unlocks automated reporting scripts. |
| **`/api/documents` + `/api/fileResources`** | Low-medium; enables attachment / capture-media workflows | Upload, list, fetch, attach-to-metadata | Separate plugin; the `customize` surface is deliberately branding-only. |
| **org-unit group sets / dimensions** | Low-medium; niche but common in analytics configs | `/api/organisationUnitGroupSets`, dimensions | Low urgency. |

### 3. Library ergonomics push (deepen what we already have)

Three high-leverage additions that sharpen the client itself, rather than adding surface:

- `client.tasks.await_completion(...)` — library-level task awaiter (currently CLI-only).
- `RetryPolicy` + backoff on `Dhis2Client` — 30 LOC, fixes a real failure mode.
- Concurrent / batch patterns example + connection-pool tuning in `docs/architecture/client.md`.

~1 cycle total, no new DHIS2 surface, noticeable quality-of-life improvement for library users.

## Near-term plan (next 3–5 PRs)

Ordered by value-per-effort, roughly:

1. **`CHANGELOG.md` + annotated git tags** — bump the workspace on every merge, tag the PyPI-publishable `dhis2-client` releases. Scaffolding for eventual public releases.
2. **More `dhis2 doctor` metadata probes** — 14 probes ship today; room to grow: indicator expression validity against `/api/expressions/validate`, OU hierarchy depth sanity, validation rules without expressions, program-indicator orphan data-element references, user accounts with no userRoles assigned.
3. **`dhis2 metadata patch <resource> <uid>`** — DHIS2 accepts RFC 6902 JSON Patch on `PATCH /api/<resource>/{uid}` for partial metadata updates (no need to round-trip the full object via PUT). `JsonPatchOp` already lives in `dhis2_client` post-#78; wiring this is: generated resource accessor `.patch(uid, ops=[...])`, service-layer `patch_metadata(resource, uid, ops)`, CLI + MCP tool. Natural follow-up to the typing work — any metadata resource becomes partially-updatable via typed op classes.
4. **Data-integrity streaming iterator** — `client.maintenance.iter_integrity_issues(...)` yielding one issue at a time for large integrity runs. Small addition to the maintenance plugin; wraps the existing `/api/dataIntegrity/details` pagination.
5. **Sweep remaining raw-client callsites in examples + diagnostic tooling** — the service-layer `get_raw`/`post_raw` calls are all wrapped in `Model.model_validate(raw)` on the next line (Bucket B carveout), but ~30 `examples/client/*` and `infra/scripts/*` raw calls could be upgraded to typed accessors on a case-by-case basis. Low-urgency follow-up to the typing sweep (#71-#74, #76).

BUGS.md #15 (undiscriminated `JobConfiguration.jobParameters` + `WebMessage.response` unions) isn't on the near-term list: the sibling-field discriminator pattern doesn't fit the AuthScheme-style spec-patches approach, and the scheduler plugin isn't an active workflow. Revisit when someone hits a real-world need.

## Medium-term

- Library-level task awaiter (`client.tasks.await_completion(...)`)
- `RetryPolicy` + backoff on `Dhis2Client`
- Concurrent-request example + connection-pool tuning note in `docs/architecture/client.md`
- Integration tests with `--watch` against the live DHIS2 stack (guard with `@pytest.mark.slow`)
- Property-based testing on filter/order DSL parsing

## Long-term / exploratory

- **`analytics.py` migration to OAS `Grid`**: the hand-written `AnalyticsResponse` / `AnalyticsHeader` / `AnalyticsMetaData` shapes don't match OpenAPI's `Grid` / `GridHeader` / `GridResponse`. Migrating forces a behaviour change on every analytics caller (row shape differs — Grid uses an index-by-position model instead of named fields). Worth doing when we next touch the analytics plugin.
- **`Notification` enum typing**: OpenAPI ships typed `category` / `dataType` / `level` enums. Wiring them would give enum autocomplete on `await_task` / `maintenance task watch` callbacks, at the cost of threading new imports through every caller. Incremental improvement; do when the next maintenance-plugin touch lands.
- **Browser-only workflows** as first-class plugins: scripted dashboard composition, visualization creation, org-unit-tree edits; anything currently only reachable through the DHIS2 web UI. Each as a `dhis2-browser` subcommand.
- **`dhis2-codegen` as a standalone PyPI package** once the emitter stabilises; lets external projects target their own DHIS2 schema. Both `/api/schemas` and OAS paths are plumbed through the same CLI now.
- **Multi-instance patterns**: `dhis2 diff <profile-a> <profile-b> <resource>` for structural comparison across environments — `metadata diff --live` already handles the single-profile-vs-file case.
- **System metadata cache**: every new `Dhis2Client` re-fetches `/api/system/info` on first call; scripts often re-fetch the default `categoryCombo` UID per run. A TTL-bounded in-memory cache (a minute or two; invalidated on write) would cut round-trips on bootstrap workflows.
- **Streaming data-value-set import**: large `dataValueSets` payloads (~100k rows, XML/CSV) currently need to be assembled in memory. `httpx` streaming uploads work; a `client.data_values.stream(source, content_type)` would unblock real-size imports.

## Reference: dhis2-java-client

Apache-2.0 Java client maintained by the DHIS2 org ([dhis2/dhis2-java-client](https://github.com/dhis2/dhis2-java-client)). Targeted comparison against this workspace as of this writing:

### Already covered here

- Typed `/api/sharing` — `Sharing`, `SharingBuilder`, `ACCESS_*` constants, `apply_sharing` / `get_sharing` helpers. Full parity with the Java client's sharing builder; used throughout the examples (e.g. `bootstrap_zero_to_data.py` step 5) instead of hand-rolled JSON Patch.
- User administration — `dhis2 user list / get / me / invite / reinvite / reset-password`. User-group + user-role plugins covering membership + authority-bundle flows.
- Branding / theming — `dhis2 dev customize logo-front/banner/style/set/apply/show` + `Dhis2Client.customize` accessor. Covers `/api/staticContent/*`, `/api/files/style`, `/api/systemSettings/*`. No equivalent in the Java client.
- Auth providers (Basic, PAT, OAuth2); ours is async-first with a typed `AuthProvider` Protocol, theirs is blocking HttpClient-based.
- Generated resource CRUD; theirs is hand-maintained Java classes; ours is schema-driven codegen across v40/v41/v42/v44.
- WebMessageResponse envelope parsing; we expose `.import_count()`, `.conflicts()`, `.rejected_indexes()`, `.task_ref()`, `.created_uid()`.
- Full metadata query surface; repeatable `--filter`, `--order`, `rootJunction=AND|OR`, `--page`/`--page-size`, `--all`, `--translate`/`--locale`, every `fields` selector form.
- **Metadata bundle export / import / diff** (beyond Java parity): `dhis2 metadata export` + `import` + `diff` with per-resource filters + dangling-reference warning on export.
- Paging; `list_raw(..., paging=True)` returns the pager; `list(..., paging=False)` walks the full catalog.
- Typed filter values on enum fields; `ValueType.NUMBER` is a `StrEnum`, substitutable into filter strings directly.
- Client-side UID generation; matches the Java `CodeGenerator` algorithm exactly.
- Typed tracker writes; `TrackerBundle` + `TrackerTrackedEntity` / `TrackerEnrollment` / `TrackerEvent` models for `POST /api/tracker`.
- Event + enrollment analytics; `dhis2 analytics events query` and `analytics enrollments query`.
- Outlier detection + tracked-entity analytics; `dhis2 analytics outlier-detection` and `analytics tracked-entities query`.

### Considered, not adopted

- **Fluent query builder (`.addFilter(Filter.eq("name", "ANC"))`)**: the Java client wraps DHIS2's `property:operator:value` string syntax in a chainable builder. Deliberately skipped — Python f-strings make `f"name:like:{name}"` already readable; the builder doesn't buy type safety on the stringly-typed value side; DHIS2's own docs teach the string form. Flagged explicitly so the decision isn't re-litigated.

### Worth evaluating later (Java parity)

- **Explicit bulk-save naming**: `.saveOrgUnits(list)` / `.saveEvents(list)` etc. We have the generic `/api/metadata` bulk path plus `service.push_tracker(bundle)` but no resource-specific `.save_events(list)` methods. Thin typed wrappers would surface bulk-write capability in IDE autocomplete.
- **File-streaming export helpers**: Java exposes `.writeAnalyticsDataValueSet(query, file)` for streaming large analytics exports to disk without buffering. We don't. Worth adding when large-export use cases surface.
- **Domain-specific response types beyond `WebMessageResponse`**: Java has distinct `PagedResponse`, `Stats`, `Response` for different endpoint shapes. We collapse all of these into `WebMessageResponse` + helpers. The OAS codegen already emits the specific shapes (`TrackerImportReport`, `ImportReport`, etc.) — swapping individual endpoints is mechanical work, mostly pending real friction on a specific call site.

### Worth evaluating later (beyond Java parity)

Items that don't exist in the Java client but would make the Python client materially more useful in practice:

- **Retry / backoff**: a typed `RetryPolicy(max_attempts, base_delay)` on `Dhis2Client` with sensible defaults costs ~30 LOC and removes a real failure mode for batch workflows. Java's HttpClient is similarly bare-bones here; this would put us ahead.
- **Library-level task awaiter**: a `client.tasks.await_completion(task_ref, ...)` helper for library callers (currently CLI-only).
- **System metadata cache**: TTL-bounded in-memory cache for `/api/system/info` + default `categoryCombo` UID.
- **Dry-run helper**: `client.metadata.dry_run(bundle)` returning a typed validation summary. Currently `service.import_metadata(..., dry_run=True)` handles this at the plugin level; promoting to the client surface would codify the two-phase pattern.
- **Bulk delete**: `.delete_bulk([uid, uid])` wrapping `/api/metadata` with `importStrategy=DELETE`.
- **Streaming data-value-set import**: `httpx` streaming uploads for large `dataValueSets` payloads.

## Explicit non-goals

- Python < 3.13. New typing features (StrEnum, TypeAliasType, PEP 604 unions) justify the bump.
- DHIS2 < v42. Every backport fork splits the code; no deployed users so no reason.
- Flask / argparse / raw stdio MCP loops / hand-rolled TOML parsers; every slot has a chosen standard per the CLAUDE.md hard-requirements list in the repo root.
- A second filter DSL layered on top of DHIS2's `property:operator:value` string syntax. See the dhis2-java-client comparison above for the rationale.
- Synchronous client variant. `async` throughout is a hard requirement.
- `dict[str, Any]` crossing module boundaries. CLAUDE.md hard rule; enforced workspace-wide as of the typing sweep (#71-#74, #76). New code that proposes dict-in-signature needs explicit justification referencing a specific HTTP-boundary carveout.

## How this file gets updated

Greenfield voice; edits describe the current state of the plan, not its history. When a near-term item ships, delete it from the "near-term" list (don't rewrite to "already shipped"). Use the PR's own description for the history; this file is always about what's next.
