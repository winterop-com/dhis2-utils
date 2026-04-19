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

Via codegen (`generated/v{40,41,42,44}`):

- 100+ metadata resources (DataElement, DataSet, OrganisationUnit, Indicator, Program, …) with full CRUD accessors
- 77+ `StrEnum`s for CONSTANT properties (ValueType, AggregationType, DataElementDomain, …)
- A shared `Reference` with both `id` and `code` fields

Hand-written in `dhis2-client`:

- `WebMessageResponse` envelope + `ObjectReport`, `ImportReport`, `ImportCount`, `Conflict`
- Tracker instance models (`TrackerTrackedEntity`, `TrackerEnrollment`, `TrackerEvent`, `TrackerRelationship`, `TrackerBundle`) + `EventStatus` / `EnrollmentStatus`, version-scoped under `dhis2_client.generated.v42.tracker` (tracker shapes drift across DHIS2 majors)
- `AnalyticsResponse` + `DataValueSet` + `DataValue`
- `AuthScheme` discriminated union (5 variants)
- `PeriodType` (24 canonical period names, class-hierarchy upstream so not emitted by codegen)
- `Notification`, `DataIntegrityCheck` + `DataIntegrityResult` + `DataIntegrityReport`

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

`09_bootstrap.py` step 5 uses a hand-coded JSON Patch to grant admin data-write access on the new dataset. DHIS2 has a coherent `sharing` block shape (public `rwrw----`, per-user, per-group); no typed helper. Common enough to deserve one.

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

- `04_oidc_login.py` fails immediately if env isn't set instead of a friendly message
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

Three fundamentally different ways to spend the next week's work. Each independently good; the right order depends on where the pain is.

### 1. Polish + incremental surface extensions (the near-term list below)

Small, low-risk PRs that tighten the existing surface. ~5 shippable items each landable in a few hours. Lowest risk, fastest visible progress. Default when there's no strategic pressure.

### 2. OpenAPI-driven generator for the remaining hand-written models

The hand-written shapes; `WebMessageResponse` + inner envelopes, `AuthScheme` union, tracker instance models, aggregate/analytics/maintenance models; are the shapes `/api/schemas` doesn't describe. DHIS2's `generated/v{N}/openapi.json` does describe them. A generator pass over the OpenAPI would:

- Emit every `components/schemas` entry as a pydantic model (alongside the existing `/api/schemas` output)
- Handle discriminated unions declaratively (kills the hand-maintained `AuthScheme` file)
- Catch DHIS2-version drift automatically (a new tracker field would appear after `dhis2 dev codegen rebuild`)
- Let us delete ~600 LOC of hand-written models once every consumer is migrated

Cost: probably a week of focused work; building a second emitter path (OpenAPI is structurally different from `/api/schemas`), migrating every caller, teaching the CLI to pick between the two sources, writing tests that pin key invariants that the `/api/schemas` path doesn't exercise.

When to pick this: if you start noticing drift between our hand-written models and what DHIS2 actually returns, or if adding a new endpoint's envelope becomes the thing that blocks feature work repeatedly.

### 3. New DHIS2 surface: expand plugin coverage

Currently: `analytics`, `data`, `dev`, `maintenance`, `metadata`, `profile`, `route`, `system`. Large adjacent domains with no dedicated plugin:

| Surface | Value | Shape | Recommend as… |
| --- | --- | --- | --- |
| **users / user-groups / user-roles** | High; near-universal admin workflow | `/api/users/*` + invite/reset/authority endpoints | **Top recommendation**; biggest real-world impact, smallest surface area. |
| **sharing** | High; unblocks the bootstrap dance | `/api/sharing` + typed `Sharing` block | **Strong second**; small lift, fixes the `09_bootstrap.py` JSON-Patch ugliness. Or combine with users as one PR. |
| **metadata export / import bundles** | Medium; needed for cross-env workflows | `/api/metadata?download` round-trips + dependency resolution | Pair with sharing (imports need sharing blocks). |
| **outlier detection + trackedEntities analytics** | Low-medium; niche but unique row shapes | `/api/analytics/outlierDetection`, `/api/analytics/trackedEntities/query` | Pair with the OpenAPI-driven-codegen push — response shapes live in OpenAPI. |
| **visualizations / dashboards / maps** | Medium; needed for UI-adjacent automation | Large surface (Visualization, Map, Dashboard, pivot tables, favourite sharing) | Save for after the tracker story is complete; these are layered on top of indicators/data. |
| **data integrity streaming** | Low; incremental polish on maintenance | `/api/dataIntegrity/details` iterator | Bundle with any other maintenance touch. |
| **validation rules / predictors** | Medium; formulas over data elements | `/api/validationRules`, `/api/predictors`, run/results | Useful once the analytics/event-analytics surface is complete. |
| **org-unit group sets / dimensions** | Low-medium; niche but common in analytics configs | `/api/organisationUnitGroupSets`, dimensions | Low urgency. |

**Recommendation if picking (3)**: start with **users + sharing** as a combined PR (~2–3 days). Both surfaces are small, both are daily-use, and sharing currently gets implemented via hand-written JSON Patch in examples; direct signal that typed coverage is missing. Event/enrollment analytics would be the natural follow-up.

## Near-term plan (next 3–5 PRs)

Ordered by value-per-effort, roughly:

1. **Sharing helper**; typed `Sharing` model (public, users{}, userGroups{}) + an `apply_sharing(client, resource, uid, sharing)` helper that PATCHes `/sharing` correctly. Rewrite `09_bootstrap.py` step 5 against it.

2. **Users plugin**; `dhis2 users list / get / invite / reset-password / grant-authority`, backed by `/api/users` + `/api/users/<uid>/invite` + `/api/users/<uid>/reset`. MCP tools to match.

3. **Metadata export/import**; `dhis2 metadata export` (download current metadata to a JSON bundle with optional filters), `dhis2 metadata import` (upload a bundle with `importStrategy` + dependency resolution). Foundation for cross-instance dev workflows.

## Medium-term

- `CHANGELOG.md` + annotated git tags on every PR merge
- GitHub Actions workflow running `make lint && make test && make docs-build` on PRs
- `dhis2 profile oidc-discovery <url>`; populate an OIDC profile from `/oauth2/authorize` metadata
- Concurrent-request example + connection-pool tuning note in `docs/architecture/client.md`
- External plugin example under `examples/plugin-external/` + a doc page walking through entry-point registration
- Integration tests with `--watch` against the live DHIS2 stack (guard with `@pytest.mark.slow`)
- Property-based testing on filter/order DSL parsing

## Long-term / exploratory

- **OpenAPI-driven generator**: replace the hand-written envelope models (`envelopes.py`, `auth_schemes.py`, `generated/v{N}/tracker.py`, `aggregate.py`, `analytics.py`, `maintenance.py`) with emitter output derived from `generated/v{N}/openapi.json`. The `/api/schemas` endpoint doesn't cover these shapes, so the generator would need to consume OpenAPI directly; non-trivial infrastructure. Most urgent for `tracker.py` since those shapes drift most across DHIS2 majors.
- **Browser-only workflows** as first-class plugins: scripted dashboard composition, visualization creation, org-unit-tree edits; anything currently only reachable through the DHIS2 web UI. Each as a `dhis2-browser` subcommand.
- **`dhis2-codegen` as a standalone PyPI package** once the emitter stabilises; lets external projects target their own DHIS2 schema.
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
- **Domain-specific response types beyond `WebMessageResponse`**: Java has distinct `PagedResponse`, `Stats`, `Response` for different endpoint shapes. We collapse all of these into `WebMessageResponse` + the helpers on it. Works today; if a specific endpoint's shape diverges materially (e.g. tracker import responses), a dedicated model is the right cut; but no concrete need yet. Likely absorbed by OpenAPI-driven codegen.

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
