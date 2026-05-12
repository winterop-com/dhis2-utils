# Changelog

## 0.11.0 — 2026-05-13

Follow-up to the v0.10.0 per-version split: v43-only Program setters land end-to-end, MCP gains a server-introspection tool, hand-written v41 enum stubs replace the last cross-version imports, and the docs site gets a full restructure — 5 top tabs (Get started / Architecture / Client / CLI / MCP), per-surface introductions, indigo theme, +400 lines of worked Python examples on the API reference pages, and an explicit "Learning path · step N of 8" framing across the canonical reading order.

### Client + plugins

- **v43-only Program setters wired end-to-end.** `programs.set_labels` (UI overrides), `programs.set_change_log_enabled` (audit toggle), `programs.set_enrollment_category_combo` (alt CC at enrollment time) — three focused methods covering the v43 `Program` schema additions (`enableChangeLog`, `enrollmentsLabel`, `eventsLabel`, `programStagesLabel`, `enrollmentCategoryCombo`). Matching CLI commands (`dhis2 metadata program set-labels / set-change-log / set-enrollment-category-combo`) and MCP tools (`metadata_program_set_labels` / `metadata_program_set_change_log_enabled` / `metadata_program_set_enrollment_category_combo`). v41/v42 don't expose these methods because the fields don't exist on those schemas (#315, #316).
- **`system_server_info` MCP tool.** Process-local introspection returning the active plugin tree (`v41` / `v42` / `v43`), the resolution chain step that picked it (`profile.version` / `DHIS2_VERSION` env / default), and the bound `dhis2w-*` package versions. Useful for agents that want to detect plugin-tree mismatch before issuing version-sensitive calls (#312).
- **v41 enum stubs.** `dhis2w_client.generated.v41.oas._enum_stubs` ships the six `StrEnum`s the v41 server doesn't surface (`AtomicMode`, `FlushMode`, `ImportStrategy`, `MergeMode`, `PreheatIdentifier`, `PreheatMode`). v41's metadata plugin no longer reaches into `generated.v42.*` to find them (#311).
- **Tracker contract tests.** Live-schema test suite extended to cover `/api/tracker/*` endpoints (trackedEntities, enrollments, events) — pulls one row from each via the corresponding accessor on `dev-2-{42,43}` and asserts it round-trips through the typed model (#313).
- **Hypothesis property tests** on the hand-written parser DSLs (UID generator + validator round-trip, period parsing + arithmetic for every absolute period kind, JsonPatch op discriminator dispatch). 17 properties run as part of the mocked test tier (#314).

### Examples

- **Three v43-only Program setter examples** (`program_set_labels.py`, `program_set_change_log.py`, `program_set_enrollment_category_combo.py`) plus the BUGS #33 CategoryCombo COC-regen workaround (`category_combo_coc_regen.py`).
- **Three v41-only divergence examples** for `oauth2_cid_field`, `apps_display_name`, `grid_rows_wire_shape` (#307).
- **`import_grouped_by_dataset` + `wait_for_coc_generation` examples** across v41/v42/v43 (#308).
- **Split bundled examples** — `validation_and_predictors.{py,sh}` -> `validation_rules.{py,sh}` + `predictors.{py,sh}`; `sharing_and_user_groups.py` -> `user_groups.py` + `user_roles.py`. Six new files; per-concern files instead of coincidence-of-version bundles (#317).
- **`open_client(profile_from_env())` standardised.** 13 client examples that used the lower-level `resolve()` + `build_auth_for_name()` + `Dhis2Client(...)` boilerplate are now on the canonical one-liner (#320). Same alignment applied to non-pinning doc code snippets (#321).
- **Raw `get_raw` replaced with typed `resources.X.list()`** where a typed accessor exists. Five example call sites converted; the audit verified the remaining 18 raw call sites are genuinely escape-hatch use (bulk imports, RFC 6902 patches, version-divergence demos) (#322).
- **Every example's `Usage:` path now version-segmented.** 328 files fixed — `uv run python examples/v42/client/whoami.py` instead of the previously copy-paste-broken unversioned form (#325).

### Documentation

- **5-tab navigation.** Top-of-page tabs (Get started / Architecture / Client / CLI / MCP) replace the previously flat 70+ item left sidebar. Each surface tab carries its own Introduction + Tutorial + Architecture + Reference. The Python API reference is sub-grouped into Core / Plugin accessors / Metadata authoring / Streaming / Utilities (#323).
- **Indigo Material theme.** Switched back to the stock `mkdocs-material` indigo palette; dropped the custom `mkdocs-claude-theme` dependency (#323).
- **Per-surface introductions** at `docs/client/index.md`, `docs/cli/index.md`, `docs/mcp/index.md`, plus a beefed-up `docs/mcp/tutorial.md` covering the full read / mutate / rollback agent workflow with explicit recovery tables.
- **API reference fleshed out.** Worked Python examples added to the 8 previously one-paragraph pages (files, messaging, aggregate, analytics-stream, envelopes, maintenance, uids, generated) and the 6 thin reference pages (auth-schemes, client, data-values, errors, tracker, validation). Every snippet verified against the v42 accessor source.
- **9 new `docs/api/` pages** for previously undocumented public modules (json-patch, categories, category-combos, category-combo-builder, category-option-combos, attribute-values, option-sets, program-rules, tasks).
- **Mermaid dependency diagram** in `docs/architecture/overview.md` + `CLAUDE.md` replaces the ASCII-arrow form.
- **`docs/examples.md`** reframed as the curated v42 catalogue + version-pinned `examples/v{41,42,43}/` trees as source of truth.
- **`docs/architecture/schema-diff-v41-v42-v43.md`** updated with the three split v43 Program setter helpers + the per-concern table (UI labels / audit toggle / alt CC).
- **Learning-path framing** on the 8 primary docs (README, walkthrough, cli-tutorial, client-tutorial, examples, api/index, architecture/overview, BUGS.md) — one-line "step N of 8" banner with prev/next links so a reader landing mid-path sees where they are.

### Workspace packages

All bumped from 0.10.0 to 0.11.0 and published to PyPI via Trusted Publishing:

- `dhis2w-client`
- `dhis2w-core`
- `dhis2w-cli`
- `dhis2w-mcp`
- `dhis2w-browser`

## 0.10.0 — 2026-05-12

Big architectural jump: per-version split of the entire workspace (v41 / v42 / v43), a 39-entry BUGS regression catalogue with 15 live verifiers, and end-to-end example verification across all three DHIS2 majors.

### Architecture

- **Per-version subpackages everywhere.** `dhis2w_client.v{41,42,43}` and `dhis2w_core.v{41,42,43}.plugins.*` are now hermetic — a v43-specific quirk lands in `v43/plugins/...` alone without touching v41/v42. Three trees seeded from the v42 baseline (#253-#272).
- **Per-version `__init__.py` re-export surfaces.** `from dhis2w_client.v41 import X` now works directly, parallel to `from dhis2w_client.v42 import X` and `from dhis2w_client.v43 import X`. The top-level `dhis2w_client` shim still routes to v42 for backwards compat with PyPI consumers (#280-#282).
- **Per-version `dhis2w-core` helpers.** `cli_errors`, `cli_output`, `cli_task_watch`, `client_context`, `oauth2_registration`, `pat_registration`, and `token_store` all have v41 / v42 / v43 copies under `dhis2w_core/v{N}/`. Shared runtime state (`JSON_OUTPUT` ContextVar, `_console` Rich singleton) stays single-source via re-exports — only the type-signature surface diverges per version (#283-#285, #289).
- **Plugin discovery resolves the version from `DHIS2_VERSION` env when `profile.version` is unset.** Lets `make verify-examples DHIS2_VERSION=41` correctly drive the v41 plugin tree without hand-editing every profile (#292).
- **Plugin retarget — all 47 plugin files per version-tree now import from their matching client subpackage** (`dhis2w_client.v{N}.*` + `dhis2w_core.v{N}.*` helpers + `dhis2w_client.generated.v{N}.*`). One hand-fix per version for genuine wire-shape divergence (#286-#288).
- **Top-level shim dropped from `dhis2w-core`-internal call paths.** Canonical imports go through `v{N}/`; the top-level remains as a PyPI-stable surface only (#271).

### v41 wire-shape adapters

- **`App.model_rebuild()` + eager forward-ref imports.** v41 subclasses `_GeneratedApp` to add the runtime-emitted `displayName` field; the parent's `defer_build=True` required explicit materialisation (#292).
- **`Grid.rows: list[list[Any]]` override.** v41 OAS declares row cells as `dict[str, Any]` but the wire carries scalars/null. Subclass widens the type to match reality (#292).
- **OAuth2 round-trip reads `cid` (BUGS.md #39).** v41 wire shape names the client identifier `cid`; v42/v43 use `clientId`. `dhis2 dev sample oauth2-client` smoke test tolerates both, preferring v41-correct `cid` on the v41 plugin tree (#262, #292).
- **Dropped `oauth2-client-credentials` auth-scheme variant.** v41's OAS and runtime don't ship it; v42/v43 do (#264).
- **`SharingObject` retargeted to `generated.v41`** with a local `Status` stub for the v41-missing enum (#269).

### v43 wire-shape adapters

- **`SharingObject.externalAccess` dropped from v43** (BUGS.md #38). v43's SharingBuilder no longer accepts `external_access` (#261).
- **`CategoryCombo.categorys` legacy alias dropped on v43** — wire writes silently no-op without `categories` (BUGS.md #34) (#260).

### BUGS regression catalogue

- **Paired bug-still-present + workaround-works tests for every BUGS.md entry.** Mocked halves run as part of `make test`; live halves run via `make test-upstream-bugs -m slow` against a docker stack (#273-#275).
- **15 live verifiers shipped** across schema reads + library-relevant writes + scope checks. Each cross-links to its BUGS.md entry and asserts the upstream bug is still observable on the wire (when DHIS2 fixes it, the test fails loudly — the signal to drop the workaround) (#276-#278, #290-#291).
- **`@pytest.mark.upstream_bug` marker + `make test-upstream-bugs` filter.** One-shot view of every workaround the codebase depends on (#273).

### Examples

- **`examples/` split into per-version directories (`examples/v{41,42,43}/{cli,client,mcp}/`).** Each version tree's examples target its matching DHIS2 major. New examples land in the version(s) where they apply (#247-#248, #272).
- **`make verify-examples DHIS2_VERSION=N`** runs every non-interactive example for major `N` and prints a PASS / FAIL / TIMEOUT / SKIP table. Currently green across all three: v41 153/0/12, v42 153/0/12, v43 158/0/12.

### Infrastructure

- **`dhis2w-codegen` accepts pinned Docker tags + restored v41 codegen tree** (#243).
- **Fresh-install seed flow** auto-disambiguates collision-prone built-in TET/TEA names (`Person (Play)`) and writes seeded PATs + OAuth2 client to `infra/home/credentials/.env.auth` (#244).
- **`make -C infra clean`** wipes volumes for clean version switches (the same Postgres volume can't host v41 then v43 — Flyway rejects unknown applied migrations).

### Coverage + CI

- **Coverage threshold honored after the per-version tripling** — v41 + v43 client / plugin trees omitted from measurement until their `tests/v{41,43}/` folders fill in (Stage 5 follow-up). Coverage on v42 + cross-version code reports 82.67% against the 70% bar (#279).

### Migration notes

- PyPI consumers using `from dhis2w_client import X` are unaffected — the top-level shim still resolves through `dhis2w_client.v42`.
- Code that imported from removed paths (`dhis2w_client.client`, `dhis2w_client.envelopes`, etc. — the pre-split layout) needs to switch to either `dhis2w_client` (top-level shim) or `dhis2w_client.v{N}.X` for version-pinned imports.
- Profiles without a `version` field continue to auto-detect on `connect()`. To pin a profile to a major, add `version = "v41"` (or `"v42"` / `"v43"`) under `[profiles.<name>]` in `profiles.toml`, or set `DHIS2_VERSION` in env when invoking `dhis2`.

## Earlier

See `git log` for releases prior to 0.10.0. Tag `v0.7.0` was the last release before the per-version split landed.
