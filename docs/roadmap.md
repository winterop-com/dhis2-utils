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

Sixteen top-level domains: `analytics`, `apps`, `browser`, `data`, `dev`, `doctor`, `files`, `maintenance`, `messaging`, `metadata`, `profile`, `route`, `system`, `user`, `user-group`, `user-role`. Each plugin shares a `service.py` between the CLI and MCP sides; the same typed call from both surfaces.

`dhis2 metadata` has the full workflow surface:

- **Core CRUD**: `list` / `get` / `patch` (RFC 6902).
- **Cross-resource search**: `dhis2 metadata search <query>` — fans out three concurrent `/api/metadata?filter=<field>:ilike:<q>` calls (`id`, `code`, `name`) and merges by UID. Full UID, partial UID, business code, or name fragment all flow through one verb.
- **Bundle operations**: `export` / `import` / `diff` (file-vs-file and file-vs-live) with per-resource filters + dangling-reference warning on export; `diff-profiles` for staging-vs-prod drift.
- **Authoring sub-apps**: `options show / find / sync` for OptionSet sync; `attribute get / set / delete / find` for cross-resource AttributeValue workflows; `program-rule show / vars-for / validate-expression / where-de-is-used`; `sql-view list / show / execute / refresh / adhoc`; `viz list / show / create / clone / delete`; `dashboard list / show / add-item / remove-item`; `map list / show / create / clone / delete`; `legend-sets list / show / create / clone / delete`; four full `X / XGroup / XGroupSet` authoring triples with canonical DHIS2 naming — `organisation-units` / `organisation-unit-groups` / `organisation-unit-group-sets` (plus `organisation-unit-levels` for per-depth rename), `data-elements` / `data-element-groups` / `data-element-group-sets`, `indicators` / `indicator-groups` / `indicator-group-sets`, and `category-options` / `category-option-groups` / `category-option-group-sets`; plus the `program-indicators` + `program-indicator-groups` pair (DHIS2 has no `programIndicatorGroupSet`).

`dhis2 doctor` runs ~100 checks on a live instance (20 metadata-health probes + 81 DHIS2 integrity checks + BUGS tripwires).

### MCP surface

243 tools across 13 plugin groups (`analytics_*`, `apps_*`, `customize_*`, `data_*`, `doctor_*`, `files_*`, `maintenance_*`, `messaging_*`, `metadata_*`, `profile_*`, `route_*`, `system_*`, `user_*`). Every CLI command has an MCP tool equivalent and vice versa; both share one typed service call.

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

The committed e2e dump (`infra/dhis-v42.sql.gz`) mirrors DHIS2 Play's Sierra Leone immunization demo with workspace-local additions: 1332 org units with GeoJSON geometries, 67 data elements, 3 indicators, 3 programs (Child Programme + Antenatal = tracker; Supervision visit = event), 2 datasets, 3 dashboards, 23 visualizations built programmatically via `VisualizationSpec` + 1 `EventVisualization` for the supervision program attached to the Immunization data dashboard, 8 maps built via `MapSpec`, 188k aggregate data values, 500 tracker entities, 12 sample supervision events covering 2024 monthly, 6 program rules + 10 program indicators. Workspace fixtures layered on top (`infra/scripts/seed/workspace_fixtures.py`): `SNOMED_CODE` attribute, `VACCINE_TYPE` option set with 5 fixed-UID options, 3 SqlViews (VIEW / QUERY / MATERIALIZED_VIEW), 2 BCG predictors + PredictorGroup + 2 output DEs, 2 BCG validation rules + ValidationRuleGroup, 4 named OrganisationUnitLevel records (Country / Province / District / Facility), 1 LegendSet (`LsDoseBand1`) attached to the Measles + Penta-1 monthly column charts. `make refresh-and-verify` wipes the stack, rebuilds the dump, runs every non-interactive example, and reports a pass/fail summary — **125 pass, 0 fail, 11 skipped** (OIDC-login flows including the Playwright-driven variant, browser screenshot captures, long-running analytics jobs, outlier detection, external httpbin dep) on the current main.

### CI

- `.github/workflows/ci.yml` runs `make lint && make test && make docs-build` on every PR
- `.github/workflows/e2e.yml` nightly — full DHIS2 stack + seeded fixtures + slow integration tests

Public distribution (PyPI, tagged releases, `CHANGELOG.md`) is explicitly out of scope — this workspace is internal-only.

### Docs

- Auto-generated **CLI reference** (`docs/cli-reference.md`, ~3700 lines from the Typer app) + **MCP reference** (`docs/mcp-reference.md`, 243 tools across 13 groups from the FastMCP server). Both regenerated on every `make docs-build`.
- **Narrative tutorials**: `docs/guides/cli-tutorial.md`, `docs/guides/client-tutorial.md`, `docs/guides/visualizations.md` (step-by-step viz + dashboard composition).
- **Examples index** (`docs/examples.md`) catalogues 138 runnable examples (67 client, 44 CLI, 27 MCP) with descriptions + cross-links to concept docs.
- **Architecture docs** cover every plugin, the client, auth, profiles, codegen, typed schemas, plugins runtime, external plugins, MCP, versioning, browser automation.
- **`BUGS.md`** — 29 upstream DHIS2 quirks with live `curl` repros + v43 re-audit status.

### Test coverage

673 tests run via `make test` (704 collected including 31 slow-marked for the nightly integration stack). Unit + CliRunner + respx-mocked HTTP. Slow tests exercise live-stack workflows (`--watch` job polling, Playwright PAT creation, dashboard screenshot capture, Playwright-driven OIDC login). `make coverage` runs branch-coverage locally but CI doesn't gate on it yet.

Test gaps:

- Property-based tests for `generate_uid` distribution (beyond the existing smoke test).
- Multi-version CI integration tests — v42 only today; v40/41/43/44 codegen is committed but never exercised against a live stack.

### Upstream quirks tracked

38 entries in the repo-root `BUGS.md`. Recent additions cover the seed / workflow cycle: DataSet Hibernate flush ordering (#23), Person-TET built-in name collisions (#24), `/api/.../metadata` leaking computed fields (#25), admin OU scope cached per session (#26), fresh-install flakiness on first metadata import (#27), `RelativePeriods` OAS schema shape (#28), `/api/metadata` ignoring `rootJunction` (#29 — the reason `metadata search` has to fan out N requests instead of one), App Hub `versions[*].created` returning epoch-millis ints instead of ISO-8601 strings (#30), and the predictor-expression parser rejecting uppercase aggregators (#31 — forces `avg()` / `sum()` lowercase even though DHIS2 docs use uppercase).

## Gaps surfaced during use

### Authoring surfaces (the big one)

The organisation-unit PR (#174) set a template — canonical DHIS2 resource names, hand-written accessors, per-item membership shortcuts, no `*Spec`. PRs #174 / #175 / #176 / #180 / #181 shipped the four analytics-authoring triples (org-units, data-elements, indicators, category-options) plus the program-indicator pair; the list below is what remains unauthored. Everything is still reachable today via generic `dhis2 metadata list / get` + the generated CRUD accessors, but nothing more. Authoring them from the CLI or MCP means hand-crafting JSON and POSTing through `metadata import`:

- **Aggregate data model**: `DataSet`, `DataSetElement`, `Section` — attaching DEs to data sets, section ordering, per-OU assignment. Paradoxically: the data-element *triple* ships (#175) but there's still no CLI path to wire those DEs into a DataSet.
- **Tracker schema**: `Program`, `ProgramStage`, `ProgramStageDataElement`, `TrackedEntityType`, `TrackedEntityAttribute`. Paradoxically: tracker *writes* are well-covered (`dhis2 tracker register / enroll / add-event`) but the schema those writes target is unauthored from the CLI.
- **Runtime-only rules**: `ValidationRule` / `ValidationRuleGroup` / `Predictor` / `PredictorGroup` can be *run* today (`maintenance validation run`, `maintenance predictors run`) but not *created* from the CLI. Seed helpers in `infra/scripts/seed/workspace_fixtures.py` show the exact payload shapes.
- **Category dimension** (the hardest corner): `Category`, `CategoryCombo`, `CategoryOptionCombo`. Tangled linkage + async regen of the CoC matrix. The `category-options` triple (#181) is the shallow half; the `Category` / `CategoryCombo` stack is a strategic option on its own (see below).

Each of these blocks is a chunk of 1-3 PRs following the OU template. Near-term plan below picks up the aggregate data model + tracker schema + validation/predictor CRUD next.

### OIDC / OAuth2 polish

- Token refresh is tested in code but undocumented for end users.
- `Local OIDC` login-page button is non-functional for browser clicks (CLI-only `redirect_url`); no per-provider "hide from login UI" flag in DHIS2 v42 — documented in `docs/architecture/auth.md`.
- Bearer-to-JSESSIONID path for browser workflows on OIDC profiles is unverified (flagged in `authenticated_session` docstring).

## Near-term plan (next 3–5 PRs)

Analytics-triples sweep is done — org-units (#174), data-elements (#175), indicators (#176), program-indicators (#180), and category-options (#181) all shipped. The near-term list picks up the other authoring gaps + the cheap-but-useful carryover items.

1. **DataSet + Section authoring** — closes the loudest gap left by the DE triples: `dhis2 metadata data-elements` can create a DE and add it to a group, but there's no CLI path to wire that DE into a `DataSet` or order it inside a `Section`. Surface: `dhis2 metadata data-sets list / show / create / add-element / remove-element / sections {add,remove,reorder}` + `client.data_sets` accessor. Per-OU assignment (the `--add-to-ou` side) is a natural second PR. Uses the same hand-written-accessor template as the triples. No triples pattern here — DataSet/Section/DataSetElement is a linked graph, not a X/XGroup/XGroupSet.
2. **Validation-rule + predictor CRUD** — the run side ships (`maintenance validation run`, `predictors run`) but creating rules and predictors still means hand-rolling JSON. Add `dhis2 metadata validation-rules {list,show,create,delete}` + `dhis2 metadata predictors {list,show,create,delete}` + `validation-rule-groups` / `predictor-groups` follow-ons. Seed helpers in `infra/scripts/seed/workspace_fixtures.py` already demonstrate the exact payload shapes — CLI is a thin wrapper. Promoted from medium-term now that the triples pattern is well established.
3. **Bulk metadata patch on the client** — `client.metadata.patch_bulk(resource, [(uid, ops), ...])` runs a list of RFC 6902 patches in one request, returns `WebMessageResponse` with per-UID status. Complements `delete_bulk` + `save_bulk`. Motivated by the now-shipped triples: operations like "rename every DataElement whose code matches" and "rewrite legendSet on a cohort of visualizations" are the natural next CLI verbs to build, and they want a bulk-patch primitive underneath.
4. **Tracker schema authoring surface** — `Program` / `ProgramStage` / `ProgramStageDataElement` / `TrackedEntityType` / `TrackedEntityAttribute` all go through generic `metadata list/get` today. Pairs poorly with the already-shipped tracker *write* plugins (`dhis2 tracker register / enroll / add-event`): you can post tracked entities but can't create the program that receives them from the CLI. Tracker schema needs dedicated sub-apps per domain (own concepts: enrollment / incident date, repeating stages, PSDE ordering) rather than `XGroup/XGroupSet` triples — probably a 2-3 PR body of work.
5. **CI coverage gate** — wire `make coverage` into `.github/workflows/ci.yml` and upload `coverage.xml` as an artifact. `pytest-cov` + `coverage[toml]` are already dev deps; `[tool.coverage.run/report]` is configured. Pure workflow YAML change; carried over for the fourth cycle now. Small + cheap; pick up when someone has 20 minutes free.

Demoted / parked:

- `apps snapshot` example + CI hook — the feature works, just the `restore --dry-run` demo still isn't in `examples/cli/apps.sh`. Low value without an active need.

BUGS.md #15 (undiscriminated `JobConfiguration.jobParameters` + `WebMessage.response` unions) stays off the near-term list: the sibling-field discriminator pattern doesn't fit the AuthScheme-style spec-patches approach, and the scheduler plugin isn't an active workflow. Revisit when someone hits a real-world need.

## Strategic options (pick one before the next cycle)

Three independent directions — the right order depends on where the pain is. Each would be a multi-PR body of work.

### 1. Category dimension authoring

The hardest corner of DHIS2 metadata: `Category` → `CategoryOption` → `CategoryCombo` → `CategoryOptionCombo`. Governs every aggregate-data-element's disaggregation (sex × age, modality × ownership, etc.). Today there's no hand-written surface — generic `metadata list/get` only. Creating a new disaggregation requires manually assembling four linked objects in the right order.

Surface:

- `dhis2 metadata category-options` / `category-option-groups` / `category-option-group-sets` — the triples pattern.
- `dhis2 metadata categories` — list / show / create / delete, with a `--options <uid>...` flag that wires options into the category on create.
- `dhis2 metadata category-combos` — list / show / create with ordered category refs. DHIS2 regenerates the matrix of `CategoryOptionCombo`s on save; the accessor should expose `wait_for_coc_generation(uid)` that polls until the expected count lands (cold-start regen can take tens of seconds on large combos).
- `dhis2 metadata category-option-combos` — read-only list / show (DHIS2 owns writes).
- Typed `CategoryComboBuilder` helper: given a list of `(category_name, [option_names])`, create every missing category + option + combo in one pass. The single most valuable authoring helper this workspace could ship.

### 2. Data approval workflow plugin

`/api/dataApprovals` + `/api/dataApprovalLevels` + `/api/dataApprovalWorkflows` cover multi-level aggregate approval (district → zone → ministry sign-off). Common in humanitarian + government reporting pipelines. Surface:

- `dhis2 dataapproval status <ds> <pe> <ou>` — which level is this cell at? `APPROVED_HERE / APPROVED_ABOVE / UNAPPROVED_READY / UNAPPROVED_WAITING`.
- `dhis2 dataapproval approve / unapprove / accept / unaccept` — the four write verbs.
- `dhis2 dataapproval bulk-status <ds> <pe>` — every org unit for one dataset-period, exit-on-incomplete mode for CI.
- Typed `DataApprovalStatus` enum + level-aware state machine.

### 3. Audit log reader

DHIS2's `/api/audits/*` endpoints track every write by user / timestamp / entity-uid (for DE values, tracker payloads, metadata changes). No wrapper today; integrations that need a "who changed X and when" history have to hand-build URLs.

- `dhis2 audit data-values --de <uid> [--ou <uid>] [--pe <pe>]` — stream every change for a cell.
- `dhis2 audit metadata --klass DataElement --uid <uid>` — metadata edit history for one resource.
- `dhis2 audit tracker-entity <uid>` — tracker write audit.
- `client.audit.iter_data_values(...)` / `iter_metadata(...)` async iterators for library callers.

Niche but valuable for compliance + forensics use cases.

## Medium-term

- **Multi-version CI matrix** — integration tests run against v42 only. Stand up v40 / v41 / v43 / v44 nightly jobs against compose-managed stacks so codegen drift gets caught before release.
- **CLI startup latency** — `dhis2 --help` takes ~2s to render, which is noticeable on every shell invocation. An explicit attempt in a `perf/lazy-oas-init` branch proved where the cost sits + why a clean fix is harder than it looked: `python -X importtime` shows ~900 ms goes into pydantic `model_rebuild` across the 562 OAS-emitted classes, triggered by 16 callers in `dhis2-client/*.py` doing `from dhis2_client.generated.v42.oas import X` at module top. A lazy PEP 562 `__getattr__` on `oas/__init__.py` is correct in isolation but every caller that imports a class by the `from oas import X` form still triggers the full load. A templates-only change saves ~80 ms; converting every caller to `from oas.<submodule> import X` saves ~1 s but breaks FastMCP's `list[Model]` tool-return serialisation (`MockValSer` instead of `SchemaSerializer` — pydantic's forward-ref resolver can't find siblings when only one submodule has been loaded, and skipping the eager `model_rebuild()` loop leaves the schemas deferred). Branch was closed rather than merged. A proper fix needs: **(a)** per-class on-demand `model_rebuild()` when the class is first touched for validate/serialize, **(b)** a namespace provider pydantic can consult lazily (maybe via `_types_namespace` + a dict proxy that imports submodules on-demand), or **(c)** accept that OAS load is unavoidable on any real command and focus on lazy plugin discovery + the Typer app-construction cost instead. Target: `dhis2 --help` under 400 ms.
- **`rootJunction=OR` client-side fallback** — BUGS.md #29: DHIS2 silently ANDs multiple `filter=` params even with `rootJunction=OR`, which is why `client.metadata.search` has to fan out three separate requests. The fan-out is a workaround, not a fix; `metadata list --filter a --filter b --root-junction OR` still quietly ANDs on the server. Add client-side OR emulation (issue one request per filter, merge by UID) behind the same `--root-junction` flag so the surface behaves as documented even while DHIS2 is broken. Gate with a `_dhis2_or_fallback` marker so the emulation can drop cleanly when the bug gets fixed upstream.
- **Property-based testing on filter / order DSL parsing.**
- **`metadata sharing bulk`** — batched variant of the existing sharing helpers. Apply one `SharingBuilder` result across many resources in one `/api/sharing` call per type.
- **`metadata merge --bundle <file>`** — feed a bundle file into the target rather than pulling from a source profile. Useful when the source is a saved export or manually-crafted bundle. Small extension to PR #171.
- **Spec-class audit: do we still need `*Spec` builders?** — every non-trivial authoring surface currently ships an `*Spec` pydantic class (`VisualizationSpec`, `MapSpec`, `MapLayerSpec`, `OptionSpec`, `LegendSetSpec`, `LegendSpec`, `AppSnapshotEntry`) that wraps the generated model with a caller-ergonomic subset. The original motivation was "generated models have 70+ fields, most are DHIS2 bookkeeping, users shouldn't have to fill them in." But: as the generated models get better (more `Optional` fields, more sensible defaults), the builder-over-model layer may be adding indirection + learning curve without buying much. The new `organisation_units.py` + `.organisation_unit_groups.py` + `.organisation_unit_group_sets.py` + `.organisation_unit_levels.py` accessors deliberately ship *without* specs — the caller passes `name`, `short_name`, `parent_uid`, etc. directly to `create_under(...)` / `create(...)` / `rename(...)`, and the accessor calls `post_raw` with a plain dict. Feels cleaner than the spec-over-model hop and gives us a concrete data point for the audit: do users miss the builder, or is keyword-arg CRUD on the accessor enough? Revisit once there's lived experience. If we keep specs, the `Spec = builder over generated model` idiom needs to be prominent in every API-reference page (already added to `api/legend-sets.md`, `api/visualizations.md`, `api/maps.md`); if we drop them, that's a breaking change that deserves its own migration PR.

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
- **Tracker authoring workflows** — `dhis2 tracker {register, enroll, add-event, outstanding}` verbs + the matching `client.tracker` helpers for operator flows beyond generic CRUD.
- **Rich conflict renderer** — `dhis2 metadata import` / `dhis2 data aggregate import` render `/api/metadata` and `/api/dataValueSets` error envelopes as a normalised `ConflictRow` table (object UID → offending property → server message).
- **Apps plugin** — `dhis2 apps {list, add, remove, update, update --all, reload, snapshot, restore, hub-list, hub-url}` + `apps_*` MCP tools + `client.apps` accessor over `/api/apps` and `/api/appHub`. `update --all --dry-run` previews available hub updates before installing; bundled core apps update in place. `hub-list --search` filters the catalog client-side. `hub-url` read/writes the `keyAppHubUrl` system setting so self-hosted hubs can be wired via CLI. `snapshot --output` pins an instance's app inventory to a portable JSON manifest; `restore <manifest>` reinstalls every hub-backed entry via `install_from_hub`, with a `--dry-run` preview that mirrors `update --all --dry-run`.
- **Metadata cross-instance merge** — `dhis2 metadata merge <source-profile> <target-profile> --resource ... [--dry-run]` orchestrates export+import in one pass, returning typed per-resource export counts plus the target import's `WebMessageResponse`. Pairs with `diff-profiles` (same resource+filter shape): diff to preview, merge to apply. Sharing blocks are stripped by default to avoid false-positive conflicts from per-instance user/group UIDs. Conflicts on the dry-run and applied paths render through the shared `ConflictRow` Rich table used by `metadata import` (#177), so preview output is immediately actionable without reaching for `--json | jq`.
- **Canonical `X / XGroup / XGroupSet` authoring triples** — sub-apps under `dhis2 metadata`, one client accessor per resource, following a single canonical-naming rule (lowercase + hyphenate the DHIS2 resource path). Shipped for `organisation-units` (#174), `data-elements` (#175), `indicators` (#176), and `category-options` (#181), plus the `program-indicators` pair (#180 — DHIS2 has no `programIndicatorGroupSet`). Each PR adds 15–19 MCP tools, full CLI verbs (`list` / `show` / `create` / rename-like / per-item membership), and hand-written accessors that return typed generated models. No `*Spec` builders — keyword args on the accessor (continues the spec-audit data point). The indicator accessor exposes `validate_expression(context="indicator")`, the program-indicator accessor `validate_expression(context="program-indicator")`, so callers can pre-flight numerator / denominator / expression references before a failed create. `category-options` additionally ships `set_validity_window(uid, start_date, end_date)` for the validity-window knob unique to that resource.
- **Playwright-driven OIDC login** — `dhis2 profile login --no-browser` prints the auth URL for copy-paste; `dhis2_browser.drive_oauth2_login(profile, user, pw)` drives the full flow via Chromium (React login → Spring AS consent → loopback redirect) for CI + headless use cases. `examples/cli/profile_oidc_login.sh` + `examples/client/oidc_login.py` auto-dispatch to the Playwright path when `DHIS2_USERNAME` / `DHIS2_PASSWORD` are in env.
- **Predictor + validation seed fixtures** — the Sierra Leone play42 snapshot now ships 2 BCG predictors (`avg` + `sum` over 3-month windows) + a PredictorGroup + 2 output DEs, plus 2 BCG validation rules + a ValidationRuleGroup that reliably produce violations. `dhis2 maintenance predictors run --group` and `dhis2 maintenance validation run --group` have concrete targets out of the box.
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
