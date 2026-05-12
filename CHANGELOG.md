# Changelog

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
