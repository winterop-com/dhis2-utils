# Roadmap

A running inventory of what the workspace covers today, gaps surfaced during use, and the near-term plan. Pre-1.0, no deployed users; every item is a judgment call about priority, not a commitment.

## Current state

### Workspace surface

| Package | Role |
| --- | --- |
| `dhis2-client` | Async HTTP client, pluggable auth, typed responses via generated models |
| `dhis2-codegen` | `/api/schemas` → pydantic + StrEnum emitter |
| `dhis2-core` | Plugin runtime + shared services (profiles, CLI errors, task watch, client context) |
| `dhis2-cli` | Typer root that discovers every plugin |
| `dhis2-mcp` | FastMCP server that mounts the same plugins |
| `dhis2-browser` | Playwright session helpers (auth through the DHIS2 login form) |

### CLI surface

Eight top-level domains: `analytics`, `data`, `dev`, `maintenance`, `metadata`, `profile`, `route`, `system`. Each plugin shares a `service.py` between the CLI and MCP sides; the same typed call from both surfaces.

### Typed models shipped

Via `/api/schemas` codegen (`generated/v{40,41,42,44}/schemas/`):

- 100+ metadata resources (DataElement, DataSet, OrganisationUnit, Indicator, Program, …) with full CRUD accessors
- 77+ `StrEnum`s for CONSTANT properties (ValueType, AggregationType, DataElementDomain, …)
- A shared `Reference` with both `id` and `code` fields

Via `/api/openapi.json` codegen (`generated/v{N}/oas/`):

- Every `components/schemas` entry — 562 classes + 260 StrEnums + 104 aliases on v42. Covers the instance-side shapes `/api/schemas` can't describe.
- Consumers in `dhis2-client`: `envelopes.py`, `auth_schemes.py`, `aggregate.py`, `system.py`, `maintenance.py`, and `generated/v42/tracker.py` are all thin shims over the OAS output.
- Emitter is deterministic + version-scoped; `dhis2 dev codegen oas-rebuild --version v{N}` regenerates from the committed `openapi.json` without network.

Remaining hand-written in `dhis2-client` (by design):

- `WebMessageResponse` subclass + `DataIntegrityReport` / `DataIntegrityResult` / `Me` / `Notification` — helper methods and client-side convenience shapes that aren't in OpenAPI (or where the OpenAPI typing would force invasive caller updates).
- `AnalyticsResponse` + `AnalyticsHeader` + `AnalyticsMetaData` — OpenAPI ships a differently-shaped `Grid` / `GridHeader` / `GridResponse`; migrating forces a behaviour change on every analytics caller. Future cleanup.
- `AuthScheme` discriminated union (5 variants) — OpenAPI ships the leaf classes but doesn't encode the `type` discriminator. The union + `AuthSchemeAdapter` + `auth_scheme_from_route` helper stay hand-defined; the 5 leaves subclass their OAS equivalents.
- `TrackerBundle` — the `POST /api/tracker` envelope isn't in OpenAPI under that name. Thin wrapper on OAS tracker models.
- `PeriodType` (24 canonical period names, class-hierarchy upstream so not emitted by either codegen path).

### Runtime features

- `--profile/-p` global override + `~/.config/dhis2/profiles.toml` or `./.dhis2/profiles.toml` auto-discovery
- `--debug/-d` global flag → stderr HTTP trace lines via `dhis2_client.http` logger
- `--watch/-w` on job-kicking commands (`analytics refresh`, `maintenance dataintegrity run`) + standalone `maintenance task watch` with Rich progress UI
- `--json` opt-in on every write command; concise one-line summary by default
- Typed `Dhis2ApiError.web_message` parses the envelope on 4xx so the CLI surfaces `conflicts[]` / `importCount` / `rejectedIndexes[]` detail
- Client-side UID generation (`generate_uid`, `generate_uids`); no `/api/system/id` round-trip

### Upstream quirks tracked

14 entries in the repo-root `BUGS.md`; analytics URL-suffix oddities, OAuth2 config cliff, soft-delete semantics, `uid` vs `id` wire-format divergence, etc. Each has a live `curl` repro.

## Gaps surfaced during use

### Sharing manipulation is raw JSON Patch

`bootstrap_zero_to_data.py` step 5 uses a hand-coded JSON Patch to grant admin data-write access on the new dataset. DHIS2 has a coherent `sharing` block shape (public `rwrw----`, per-user, per-group); no typed helper. Common enough to deserve one.

### Users / UserGroups / UserRoles have no plugin

The resources are generated so `client.resources.users.list()` works. But `dhis2 users invite / reset-password / grant-authority` would collapse a bunch of scripted workflows into a plugin. Same for UserGroups (sharing) and UserRoles (authority bundles).

### No metadata export/import bundles

`/api/metadata?download=true` returns a full or filtered metadata dump for round-tripping across instances. The bulk-import path is wrapped minimally (`10_metadata_bulk_import.py` demo); there's no `dhis2 metadata export` / `metadata import` pair with file-based handoff, dependency resolution, or diff-against-target views.

### Analytics endpoints without typed coverage

`dhis2 analytics query`, `analytics events query`, `analytics enrollments query` cover the three core shapes. Still missing: `/api/analytics/outlierDetection` and `/api/analytics/trackedEntities/query`. Both have response shapes distinct from the aggregate and event paths and warrant separate typed models.

### No typed `/api/dataIntegrity/issues` iterator

Currently `dataintegrity result --details` returns the full `DataIntegrityReport` as a dict-wrapped pydantic model. Large integrity runs (1000s of issues) would benefit from a streaming iterator.

### Plugin system has no demonstrable external example

`pyproject.toml` entry-point registration for external plugins is documented but the pattern isn't exercised anywhere in the repo. A tiny `dhis2-plugin-example/` showing how to publish a standalone plugin would reduce onboarding friction.

### dhis2-browser has one user and no follow-on

The screenshot plugin was the initial consumer. No UI-automation examples for the commonly-asked workflows (e.g. scripted dashboard creation, imports/exports through the web UI when the API path is blocked). Potential future surface.

### Release engineering

- No `CHANGELOG.md`
- `make publish-client` exists in the Makefile but hasn't been exercised
- No version tags on git
- No GitHub Actions CI config for running `make lint && make test` on PRs

### OIDC / OAuth2 polish

- `oidc_login.py` fails immediately if env isn't set instead of a friendly message
- Token refresh is tested in code but undocumented for end users
- No `dhis2 profile oidc-config <url>` helper that writes a profile from a `/oauth2/authorize` discovery URL

### Concurrent / bulk patterns

No example showing `asyncio.gather` against the client, no guidance on connection-pool sizing for batch workflows. `examples/client/20_concurrent.py` or similar.

### Test coverage

47 test files covering 6 packages. Gaps:

- Property-based tests for `generate_uid` distribution (beyond the existing smoke test)
- Integration tests that exercise `--watch` end-to-end against the live DHIS2 stack (currently only unit-mocked)
- No tests for `dhis2-browser`'s login-form flow (Playwright isolation keeps it out of `make test`)

## Strategic options (pick one before the next cycle)

Two fundamentally different ways to spend the next week's work. Each independently good; the right order depends on where the pain is.

### 1. Polish + incremental surface extensions (the near-term list below)

Small, low-risk PRs that tighten the existing surface. ~5 shippable items each landable in a few hours. Lowest risk, fastest visible progress. Default when there's no strategic pressure.

### 2. New DHIS2 surface: expand plugin coverage

Currently: `analytics`, `data`, `dev`, `maintenance`, `metadata`, `profile`, `route`, `system`. Large adjacent domains with no dedicated plugin:

| Surface | Value | Shape | Recommend as… |
| --- | --- | --- | --- |
| **users / user-groups / user-roles** | High; near-universal admin workflow | `/api/users/*` + invite/reset/authority endpoints | **Top recommendation**; biggest real-world impact, smallest surface area. |
| **sharing** | High; unblocks the bootstrap dance | `/api/sharing` + typed `Sharing` block | **Strong second**; small lift, fixes the `bootstrap_zero_to_data.py` JSON-Patch ugliness. Or combine with users as one PR. |
| **metadata export / import bundles** | Medium; needed for cross-env workflows | `/api/metadata?download` round-trips + dependency resolution | Pair with sharing (imports need sharing blocks). |
| **outlier detection + trackedEntities analytics** | Low-medium; niche but unique row shapes | `/api/analytics/outlierDetection`, `/api/analytics/trackedEntities/query` | Models already emitted by OAS codegen; the work is threading them into the analytics plugin service/CLI. |
| **visualizations / dashboards / maps** | Medium; needed for UI-adjacent automation | Large surface (Visualization, Map, Dashboard, pivot tables, favourite sharing) | Save for after the tracker story is complete; these are layered on top of indicators/data. |
| **data integrity streaming** | Low; incremental polish on maintenance | `/api/dataIntegrity/details` iterator | Bundle with any other maintenance touch. |
| **validation rules / predictors** | Medium; formulas over data elements | `/api/validationRules`, `/api/predictors`, run/results | Useful once the analytics/event-analytics surface is complete. |
| **org-unit group sets / dimensions** | Low-medium; niche but common in analytics configs | `/api/organisationUnitGroupSets`, dimensions | Low urgency. |

**Recommendation if picking (2)**: start with **users + sharing** as a combined PR (~2–3 days). Both surfaces are small, both are daily-use, and sharing currently gets implemented via hand-written JSON Patch in examples; direct signal that typed coverage is missing. Outlier detection and trackedEntities analytics are the natural follow-up — the typed models already ship via OAS codegen, so wiring them is service-layer only.

## Near-term plan (next 3–5 PRs)

Ordered by value-per-effort, roughly:

1. **Metadata export/import**; `dhis2 metadata export` (download current metadata to a JSON bundle with optional filters), `dhis2 metadata import` (upload a bundle with `importStrategy` + dependency resolution). Foundation for cross-instance dev workflows.

## Medium-term

- `CHANGELOG.md` + annotated git tags on every PR merge
- GitHub Actions workflow running `make lint && make test && make docs-build` on PRs
- `dhis2 profile oidc-discovery <url>`; populate an OIDC profile from `/oauth2/authorize` metadata
- Concurrent-request example + connection-pool tuning note in `docs/architecture/client.md`
- External plugin example under `examples/plugin-external/` + a doc page walking through entry-point registration
- Integration tests with `--watch` against the live DHIS2 stack (guard with `@pytest.mark.slow`)
- Property-based testing on filter/order DSL parsing

## Long-term / exploratory

- **`analytics.py` migration to OAS `Grid`**: the hand-written `AnalyticsResponse` / `AnalyticsHeader` / `AnalyticsMetaData` shapes don't match OpenAPI's `Grid` / `GridHeader` / `GridResponse`. Migrating forces a behaviour change on every analytics caller (row shape differs — Grid uses an index-by-position model instead of named fields). Worth doing when we next touch the analytics plugin.
- **`Notification` enum typing**: OpenAPI ships typed `category` / `dataType` / `level` enums. Wiring them would give enum autocomplete on `await_task` / `maintenance task watch` callbacks, at the cost of threading new imports through every caller. Incremental improvement; do when the next maintenance-plugin touch lands.
- **Browser-only workflows** as first-class plugins: scripted dashboard composition, visualization creation, org-unit-tree edits; anything currently only reachable through the DHIS2 web UI. Each as a `dhis2-browser` subcommand.
- **`dhis2-codegen` as a standalone PyPI package** once the emitter stabilises; lets external projects target their own DHIS2 schema. Both `/api/schemas` and OAS paths are plumbed through the same CLI now.
- **Multi-instance patterns**: `dhis2 diff <profile-a> <profile-b> <resource>` for structural comparison across environments.

## Reference: dhis2-java-client

Apache-2.0 Java client maintained by the DHIS2 org ([dhis2/dhis2-java-client](https://github.com/dhis2/dhis2-java-client)). Targeted comparison against this workspace as of this writing:

### Already covered here

- Auth providers (Basic, PAT, OAuth2); ours is async-first with a typed `AuthProvider` Protocol, theirs is blocking HttpClient-based.
- Generated resource CRUD; theirs is hand-maintained Java classes; ours is schema-driven codegen across v40/v41/v42/v44. Generated models are version-scoped (`dhis2_client.generated.v{N}.schemas`) so major-version drift lands as a parallel directory rather than a source-level rewrite.
- WebMessageResponse envelope parsing; we expose `.import_count()`, `.conflicts()`, `.rejected_indexes()`, `.task_ref()`, `.created_uid()` which covers the Java `Response` / `Stats` surface.
- Full metadata query surface; repeatable `--filter`, `--order`, `rootJunction=AND|OR`, `--page`/`--page-size`, `--all` (server-side paging walk), `--translate`/`--locale`, and every `fields` selector form (`:identifiable`, `:all,!prop`, `children[id,name]`). Matches the Java builder's coverage without the second DSL.
- Paging; `list_raw(..., paging=True)` returns the pager; `list(..., paging=False)` walks the full catalog.
- Typed filter values on enum fields; `ValueType.NUMBER` is a `StrEnum`, substitutable into filter strings directly.
- Client-side UID generation; matches the Java `CodeGenerator` algorithm exactly.
- Typed tracker writes; `TrackerBundle` + `TrackerTrackedEntity` / `TrackerEnrollment` / `TrackerEvent` models for `POST /api/tracker`. Java exposes individual `.saveEvents(list)` methods; ours funnel through one bundle that matches the DHIS2 wire shape.
- Event + enrollment analytics; `dhis2 analytics events query` and `analytics enrollments query` cover `/api/analytics/{events,enrollments}/query` with all dimension/filter/output-type flags.

### Considered, not adopted

- **Fluent query builder (`.addFilter(Filter.eq("name", "ANC"))`)**: the Java client wraps DHIS2's `property:operator:value` string syntax in a chainable builder. Deliberately skipped here (see non-goals below): Python f-strings make `f"name:like:{name}"` already readable; the builder doesn't buy type safety on the stringly-typed value side; DHIS2's own docs teach the string form; every review would re-suggest the wrapper otherwise. Flagged explicitly so the decision isn't re-litigated.

### Worth evaluating later (Java parity)

- **Explicit bulk-save naming**: the Java client exposes `.saveOrgUnits(list)`, `.saveEvents(list)`, etc. We have a generic `/api/metadata` bulk path plus `service.push_tracker(bundle)` but no resource-specific `.save_events(list)` / `.save_tracked_entities(list)` methods. A thin typed wrapper per collection would surface bulk-write capability in IDE autocomplete.
- **File-streaming export helpers**: Java exposes `.writeAnalyticsDataValueSet(query, file)` for streaming large analytics exports to disk without buffering. We don't; callers capture the full response in memory. If large analytics exports become a frequent use case, a streaming variant is worth adding.
- **Domain-specific response types beyond `WebMessageResponse`**: Java has distinct `PagedResponse`, `Stats`, `Response` for different endpoint shapes. We collapse all of these into `WebMessageResponse` + the helpers on it. The OAS codegen already emits the specific shapes (`TrackerImportReport`, `ImportReport`, etc.) — swapping individual endpoints to their typed responses is mechanical work, mostly pending real friction on a specific call site.

### Worth evaluating later (beyond Java parity)

Items that don't exist in the Java client but would make the Python client materially more useful in practice:

- **Retry / backoff**: no HTTP retry on transient 5xx or connection resets. `httpx` exposes the hooks cleanly; a typed `RetryPolicy(max_attempts, base_delay)` on `Dhis2Client` with sensible defaults costs ~30 LOC and removes a real failure mode for batch workflows. Java's HttpClient is similarly bare-bones here; this would put us ahead.
- **Library-level task awaiter**: `--watch` is CLI-only (`dhis2-core/task_watcher.py`). A `client.tasks.await_completion(task_ref, *, timeout, poll_interval)` helper would let library callers block on analytics refreshes / metadata imports / data integrity runs without reaching into the plugin layer. Small wrap around the existing service.
- **System metadata cache**: every new `Dhis2Client` re-fetches `/api/system/info` on first call, and callers often re-fetch the default `categoryCombo` UID per script. A TTL-bounded in-memory cache (a minute or two; invalidated on write) would cut round-trips noticeably on bootstrap scripts.
- **Dry-run helper**: `/api/metadata?importStrategy=...&dryRun=true` is the canonical way to validate a bundle before committing; currently callers pass `params={"dryRun": "true"}` by hand (see `10_metadata_bulk_import.py`). A `client.metadata.dry_run(bundle)` that returns a typed validation summary would codify the two-phase pattern.
- **Bulk delete**: no `.delete_bulk([uid, uid])` — callers loop over single deletes. DHIS2 accepts a bulk payload at `/api/metadata` with `importStrategy=DELETE`. Worth wrapping once a cleanup workflow exists.
- **Streaming data-value-set import**: large `dataValueSets` payloads (~100k rows, XML/CSV) currently need to be assembled in memory then POSTed. `httpx` streaming uploads work; a `client.data_values.stream(source, content_type)` would unblock real-size imports.

## Explicit non-goals

- Python < 3.13. New typing features (StrEnum, TypeAliasType, PEP 604 unions) justify the bump.
- DHIS2 < v42. Every backport fork splits the code; no deployed users so no reason.
- Flask / argparse / raw stdio MCP loops / hand-rolled TOML parsers; every slot has a chosen standard per the CLAUDE.md hard-requirements list in the repo root.
- A second filter DSL layered on top of DHIS2's `property:operator:value` string syntax. The string is what the docs teach and Python f-strings already make the form readable; wrapping doesn't buy type safety on the value side. The Java client ships a `Filter.eq()` / `.like()` builder; we deliberately don't mirror it. See the dhis2-java-client comparison above.
- Synchronous client variant. `async` throughout is a hard requirement.

## How this file gets updated

Greenfield voice; edits describe the current state of the plan, not its history. When a near-term item ships, delete it from the "near-term" list (don't rewrite to "already shipped"). Use the PR's own description for the history; this file is always about what's next.
