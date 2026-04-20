# Examples index

Every example in `examples/` catalogued in one place. Each entry: **file path → what it demonstrates → which concept doc explains it**.

Examples come in three flavours:

- **CLI** (`examples/cli/*.sh`) — bash invocations of the `dhis2` Typer CLI. Run with `bash examples/cli/<name>.sh` with the venv on `PATH` (via `source .venv/bin/activate` or `uv run -- bash ...`).
- **Client** (`examples/client/*.py`) — Python library usage. Run with `uv run python examples/client/<name>.py`.
- **MCP** (`examples/mcp/*.py`) — FastMCP tool calls through an in-process client. Run with `uv run python examples/mcp/<name>.py`.

Every example reads the active DHIS2 profile from `.dhis2/profiles.toml` / `~/.config/dhis2/profiles.toml` / `DHIS2_PROFILE` env (see [profiles](architecture/profiles.md)). Assume a seeded local stack (`make dhis2-run`) unless stated otherwise.

## CLI examples

| Example | What it demonstrates | Related docs |
| --- | --- | --- |
| [`metadata_round_trip.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/metadata_round_trip.sh) | **Cookbook** — export → jq transform → diff → dry-run → import → live verify → revert | [CLI tutorial](guides/cli-tutorial.md) / [metadata plugin](architecture/metadata-plugin.md) |
| [`whoami.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/whoami.sh) | Simplest invocation — `dhis2 system whoami` + `dhis2 system info` | [system](architecture/system.md) |
| [`profile_list_verify.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/profile_list_verify.sh) | `dhis2 profile list / verify / show` | [profiles](architecture/profiles.md) |
| [`profile_oidc_config.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/profile_oidc_config.sh) | Populate an OAuth2 profile by discovering DHIS2's OIDC endpoints | [auth](architecture/auth.md) |
| [`profile_oidc_login.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/profile_oidc_login.sh) | Full OIDC login flow — profile add → login → verify → whoami | [auth](architecture/auth.md) |
| [`metadata_list_get.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/metadata_list_get.sh) | `dhis2 metadata list` / `get` + client-side UID generation | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_patch.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/metadata_patch.sh) | RFC 6902 JSON Patch — inline `--set` / `--remove` and file-based | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_export_import.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/metadata_export_import.sh) | Cross-instance bundle round-trip (export → import) | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_export_filter.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/metadata_export_filter.sh) | Per-resource filters + dangling-reference warning on export | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_diff.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/metadata_diff.sh) | `dhis2 metadata diff` — bundle-vs-bundle or bundle-vs-live | [metadata plugin](architecture/metadata-plugin.md) |
| [`aggregate_data_values.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/aggregate_data_values.sh) | Aggregate data values — read / write a single value / bulk file push | [aggregate](architecture/aggregate.md) |
| [`tracker_reads.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/tracker_reads.sh) | Tracked entities by type, enrollments, events, bulk import | [tracker](architecture/tracker.md) |
| [`analytics_query.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/analytics_query.sh) | Aggregated analytics queries + resource-table refresh | [analytics](architecture/analytics.md) |
| [`analytics_outlier_tracked_entities.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/analytics_outlier_tracked_entities.sh) | Outlier detection + tracked-entity analytics | [analytics](architecture/analytics.md) |
| [`user_administration.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/user_administration.sh) | `dhis2 user` — list / get / invite / reinvite / reset-password | [user plugin](architecture/user-plugin.md) |
| [`user_groups_and_roles.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/user_groups_and_roles.sh) | `dhis2 user-group` + `dhis2 user-role` admin workflows | [user groups + roles](architecture/user-groups-and-roles.md) |
| [`route_register_and_run.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/route_register_and_run.sh) | `dhis2 route` lifecycle across every upstream auth type | [auth schemes](api/auth-schemes.md) |
| [`customize_login.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/customize_login.sh) | Brand the DHIS2 login page + top menu | [customize plugin](architecture/customize-plugin.md) |
| [`doctor.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/doctor.sh) | `dhis2 doctor` — probe every BUGS.md gotcha + metadata-health check | [doctor plugin](architecture/doctor-plugin.md) |
| [`maintenance.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/maintenance.sh) | `dhis2 maintenance` — background tasks, cache, cleanup, integrity | [maintenance plugin](architecture/maintenance-plugin.md) |
| [`dev_codegen.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/dev_codegen.sh) | `dhis2 dev codegen` — regenerate the typed client from a live instance | [codegen](codegen.md) |
| [`dev_pat.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/dev_pat.sh) | `dhis2 dev pat create` — provision a PAT as admin | [auth](architecture/auth.md) |
| [`dev_sample.sh`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/cli/dev_sample.sh) | `dhis2 dev sample ...` — inject fixtures + verify end-to-end | [manual testing](manual-testing.md) |

## Client examples (Python library)

| Example | What it demonstrates | Related docs |
| --- | --- | --- |
| [`bulk_patch_from_csv.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/bulk_patch_from_csv.py) | **Cookbook** — apply a CSV of patches concurrently via `asyncio.gather` + `JsonPatchOpAdapter` | [metadata plugin](architecture/metadata-plugin.md) |
| [`profile_drift_check.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/profile_drift_check.py) | **Cookbook** — diff metadata between two profiles, exit non-zero on drift (CI template) | [metadata plugin](architecture/metadata-plugin.md) |
| [`retry_policy.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/retry_policy.py) | **Cookbook** — `RetryPolicy` for transient 5xx / connection errors on batch workflows | [client library tutorial](guides/client-tutorial.md) |
| [`task_await.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/task_await.py) | **Cookbook** — `client.tasks.await_completion` blocks on analytics refresh / metadata import / etc. | [client library tutorial](guides/client-tutorial.md) |
| [`concurrent_bulk.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/concurrent_bulk.py) | **Cookbook** — fan-out patterns (naive gather → bounded semaphore → tuned pool + retries) with live timings | [client architecture](architecture/client.md) |
| [`integrity_issues_stream.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/integrity_issues_stream.py) | **Cookbook** — `client.maintenance.iter_integrity_issues` streams tagged issues, severity histogram, early-break scan | [maintenance plugin](architecture/maintenance-plugin.md) |
| [`system_cache.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/system_cache.py) | **Cookbook** — `client.system` cache: `info()` primed on connect, `default_category_combo_uid()`, per-key `setting()`, invalidate + refetch | [system API](api/system.md) |
| [`whoami.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/whoami.py) | Minimal — default profile → call `/api/me` | [client library tutorial](guides/client-tutorial.md) |
| [`library_only_auth.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/library_only_auth.py) | Library-only auth for PyPI consumers without `dhis2-core` | [auth](architecture/auth.md) |
| [`profile_resolver.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/profile_resolver.py) | Use a DHIS2 profile from Python via `dhis2-core.open_client` | [profiles](architecture/profiles.md) |
| [`profile_crud.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/profile_crud.py) | Profile CRUD — in-memory `Profile(...)` + on-disk `add/rename/set-default/remove` through the profile-plugin service | [profiles](architecture/profiles.md) |
| [`oidc_login.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/oidc_login.py) | Interactive OAuth 2.1 authorization-code + PKCE flow | [auth](architecture/auth.md) |
| [`list_data_elements.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/list_data_elements.py) | Generated typed resource accessors | [metadata CRUD](architecture/metadata-crud.md) |
| [`enum_round_trip.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/enum_round_trip.py) | Generated StrEnums — type-safe access to DHIS2 CONSTANT values | [typed schemas](architecture/typed-schemas.md) |
| [`metadata_filter_order_paging.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/metadata_filter_order_paging.py) | Full query DSL — filters, rootJunction, order, server-side paging | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_patch.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/metadata_patch.py) | RFC 6902 JSON Patch — generated accessor + service + adapter paths | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_export_import.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/metadata_export_import.py) | Export + import round-trip via the service layer | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_diff.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/metadata_diff.py) | `service.diff_bundles` + `diff_bundle_against_instance` | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_bulk_import.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/metadata_bulk_import.py) | Typed dry-run + real bulk import | [metadata plugin](architecture/metadata-plugin.md) |
| [`indicator_crud.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/indicator_crud.py) | Create a typed Indicator with a formula, use it, clean up | [metadata CRUD](architecture/metadata-crud.md) |
| [`data_set_crud.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/data_set_crud.py) | Full CRUD lifecycle for a data set | [metadata CRUD](architecture/metadata-crud.md) |
| [`org_unit_crud.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/org_unit_crud.py) | Full CRUD lifecycle for an organisation unit | [metadata CRUD](architecture/metadata-crud.md) |
| [`geojson_org_units.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/geojson_org_units.py) | Pull org units as GeoJSON (validated via geojson-pydantic) | [metadata CRUD](architecture/metadata-crud.md) |
| [`push_data_value.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/push_data_value.py) | Write one aggregate data value against the seeded dataset | [aggregate](architecture/aggregate.md) |
| [`tracker_lifecycle.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/tracker_lifecycle.py) | Create a tracked entity with an enrollment + event | [tracker](architecture/tracker.md) |
| [`analytics_query.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/analytics_query.py) | Aggregated analytics + resource-table refresh | [analytics](architecture/analytics.md) |
| [`analytics_events_enrollments.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/analytics_events_enrollments.py) | Event + enrollment analytics queries | [analytics](architecture/analytics.md) |
| [`analytics_outlier_tracked_entities.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/analytics_outlier_tracked_entities.py) | Outlier detection + tracked-entity analytics | [analytics](architecture/analytics.md) |
| [`task_polling.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/task_polling.py) | Watch an analytics-refresh job to completion | [maintenance plugin](architecture/maintenance-plugin.md) |
| [`doctor.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/doctor.py) | Programmatic probe results for CI / monitoring | [doctor plugin](architecture/doctor-plugin.md) |
| [`user_administration.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/user_administration.py) | User administration via the Python client | [user plugin](architecture/user-plugin.md) |
| [`user_groups_and_roles.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/user_groups_and_roles.py) | User groups + user roles via the Python client | [user groups + roles](architecture/user-groups-and-roles.md) |
| [`sharing.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/sharing.py) | Typed sharing helpers — read + replace on any object | [sharing](api/sharing.md) |
| [`customize_login.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/customize_login.py) | Brand a DHIS2 instance programmatically | [customize plugin](architecture/customize-plugin.md) |
| [`error_handling.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/error_handling.py) | `Dhis2ApiError`, WebMessage conflicts, `AuthenticationError` | [errors](api/errors.md) |
| [`bootstrap_zero_to_data.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/client/bootstrap_zero_to_data.py) | End-to-end — zero org unit to a data value in one script | [client library tutorial](guides/client-tutorial.md) |

## MCP examples

| Example | What it demonstrates | Related docs |
| --- | --- | --- |
| [`whoami.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/whoami.py) | `whoami` + `system_info` MCP tools in-process | [MCP](architecture/mcp.md) |
| [`profile_tools.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/profile_tools.py) | Read-only `profile` MCP tools | [profiles](architecture/profiles.md) |
| [`metadata.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/metadata.py) | Browse metadata via MCP | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_patch.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/metadata_patch.py) | RFC 6902 JSON Patch via the `metadata_patch` tool | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_diff.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/metadata_diff.py) | `metadata_diff` tool against two bundles | [metadata plugin](architecture/metadata-plugin.md) |
| [`metadata_export_import.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/metadata_export_import.py) | Bundle round-trip via MCP tools | [metadata plugin](architecture/metadata-plugin.md) |
| [`aggregate_data_values.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/aggregate_data_values.py) | GET / SET / DELETE data values via MCP | [aggregate](architecture/aggregate.md) |
| [`tracker_reads.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/tracker_reads.py) | Discover TET types, list entities/events via MCP | [tracker](architecture/tracker.md) |
| [`analytics_query.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/analytics_query.py) | Aggregated analytics + refresh via MCP | [analytics](architecture/analytics.md) |
| [`analytics_events_enrollments.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/analytics_events_enrollments.py) | Event + enrollment analytics via MCP | [analytics](architecture/analytics.md) |
| [`analytics_outlier_tracked_entities.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/analytics_outlier_tracked_entities.py) | Outlier detection + tracked-entity analytics via MCP | [analytics](architecture/analytics.md) |
| [`maintenance.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/maintenance.py) | Tasks, cache, cleanup, data-integrity via MCP | [maintenance plugin](architecture/maintenance-plugin.md) |
| [`route_register_and_run.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/route_register_and_run.py) | Route CRUD + run via MCP | [auth schemes](api/auth-schemes.md) |
| [`doctor.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/doctor.py) | Structured probe results for an agent via `doctor_run` | [doctor plugin](architecture/doctor-plugin.md) |
| [`user_administration.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/user_administration.py) | User plugin MCP tools | [user plugin](architecture/user-plugin.md) |
| [`sharing_and_user_groups.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/sharing_and_user_groups.py) | Sharing + user-group admin via MCP | [user groups + roles](architecture/user-groups-and-roles.md) |
| [`customize_login.py`](https://github.com/winterop-com/dhis2-utils/blob/main/examples/mcp/customize_login.py) | Branding via MCP | [customize plugin](architecture/customize-plugin.md) |

## External plugin example

[`examples/plugin-external/`](https://github.com/winterop-com/dhis2-utils/tree/main/examples/plugin-external) — a minimal runnable external plugin (own `pyproject.toml`, entry-point registration, CLI + MCP hooks). See [external plugins](architecture/external-plugin.md) for the contract.

## How example coverage maps to features

- **Every top-level CLI domain has at least one example.** See [CLI reference](cli-reference.md) for the full command tree.
- **Every plugin with a service layer has both a CLI and client example.** Pairs are intentional — the CLI shows the user-facing path, the client shows what library callers do.
- **Every MCP tool has at least one example call** showing the expected input shape + how to unpack the `structured_content` return.

When adding a new plugin / command / MCP tool: update this file alongside the feature PR so the catalogue stays in sync.
