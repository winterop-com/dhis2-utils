# MCP reference

Every tool exposed by the `dhis2` FastMCP server, grouped by plugin. Auto-generated from the in-process server — do not edit by hand. Rebuild via `make docs-mcp` (chained into `make docs-build`).

**Total tools**: 72 across 10 plugin groups.

## Plugins

- [`analytics_*`](#analytics) — 6 tools
- [`customize_*`](#customize) — 7 tools
- [`data_*`](#data) — 11 tools
- [`doctor_*`](#doctor) — 4 tools
- [`maintenance_*`](#maintenance) — 8 tools
- [`metadata_*`](#metadata) — 7 tools
- [`profile_*`](#profile) — 4 tools
- [`route_*`](#route) — 7 tools
- [`system_*`](#system) — 2 tools
- [`user_*`](#user) — 16 tools

## `analytics`

### `analytics_enrollments_query`

Run an enrollment analytics query at /api/analytics/enrollments/query/{program}.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program` | `string` | yes | — |
| `dimensions` | `list[string]` | no | — |
| `filters` | `list[string]` | no | — |
| `start_date` | `string` | no | — |
| `end_date` | `string` | no | — |
| `skip_meta` | `boolean` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `analytics_events_query`

Run an event analytics query at /api/analytics/events/{mode}/{program}.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program` | `string` | yes | — |
| `mode` | `string` | no | — |
| `dimensions` | `list[string]` | no | — |
| `filters` | `list[string]` | no | — |
| `stage` | `string` | no | — |
| `output_type` | `string` | no | — |
| `start_date` | `string` | no | — |
| `end_date` | `string` | no | — |
| `skip_meta` | `boolean` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `analytics_outlier_detection`

Run `/api/analytics/outlierDetection` — flag anomalous data values.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `data_elements` | `list[string]` | no | — |
| `data_sets` | `list[string]` | no | — |
| `org_units` | `list[string]` | no | — |
| `periods` | `string` | no | — |
| `start_date` | `string` | no | — |
| `end_date` | `string` | no | — |
| `algorithm` | `string` | no | — |
| `threshold` | `number` | no | — |
| `max_results` | `integer` | no | — |
| `order_by` | `string` | no | — |
| `sort_order` | `string` | no | — |
| `profile` | `string` | no | — |

### `analytics_query`

Run a DHIS2 analytics query.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dimensions` | `list[string]` | yes | — |
| `shape` | `string` | no | — |
| `filters` | `list[string]` | no | — |
| `aggregation_type` | `string` | no | — |
| `output_id_scheme` | `string` | no | — |
| `include_num_den` | `boolean` | no | — |
| `display_property` | `string` | no | — |
| `start_date` | `string` | no | — |
| `end_date` | `string` | no | — |
| `skip_meta` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `analytics_refresh`

Trigger analytics-table regeneration via POST /api/resourceTables/analytics.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `skip_resource_tables` | `boolean` | no | — |
| `last_years` | `integer` | no | — |
| `profile` | `string` | no | — |

### `analytics_tracked_entities_query`

Line-list tracked entities via `/api/analytics/trackedEntities/query/{trackedEntityType}`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `tracked_entity_type` | `string` | yes | — |
| `dimensions` | `list[string]` | no | — |
| `filters` | `list[string]` | no | — |
| `program` | `list[string]` | no | — |
| `start_date` | `string` | no | — |
| `end_date` | `string` | no | — |
| `ou_mode` | `string` | no | — |
| `display_property` | `string` | no | — |
| `skip_meta` | `boolean` | no | — |
| `skip_data` | `boolean` | no | — |
| `include_metadata_details` | `boolean` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `asc` | `list[string]` | no | — |
| `desc` | `list[string]` | no | — |
| `profile` | `string` | no | — |

## `customize`

### `customize_apply`

Apply a committed preset directory in one call.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `directory` | `string` | yes | — |
| `profile` | `string` | no | — |

### `customize_logo_banner`

Upload an image file as the DHIS2 top-menu banner logo (authenticated pages).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | yes | — |
| `profile` | `string` | no | — |

### `customize_logo_front`

Upload an image file as the DHIS2 login-page splash / upper-right logo.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | yes | — |
| `profile` | `string` | no | — |

### `customize_set_setting`

Set a single DHIS2 system setting.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | yes | — |
| `value` | `string` | yes | — |
| `profile` | `string` | no | — |

### `customize_set_settings`

Bulk-set DHIS2 system settings from a `{key: value}` mapping; returns keys applied.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `settings` | `object` | yes | — |
| `profile` | `string` | no | — |

### `customize_show`

Return DHIS2's read-only `/api/loginConfig` summary (what the login app renders).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `customize_style`

Upload a CSS file served as `/api/files/style` on every authenticated page.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | yes | — |
| `profile` | `string` | no | — |

## `data`

### `data_aggregate_delete`

Delete a single aggregate data value via DELETE /api/dataValues.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `data_element` | `string` | yes | — |
| `period` | `string` | yes | — |
| `org_unit` | `string` | yes | — |
| `category_option_combo` | `string` | no | — |
| `attribute_option_combo` | `string` | no | — |
| `profile` | `string` | no | — |

### `data_aggregate_get`

Fetch a DHIS2 aggregate data value set.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `data_set` | `string` | no | — |
| `period` | `string` | no | — |
| `start_date` | `string` | no | — |
| `end_date` | `string` | no | — |
| `org_unit` | `string` | no | — |
| `children` | `boolean` | no | — |
| `data_element_group` | `string` | no | — |
| `limit` | `integer` | no | — |
| `profile` | `string` | no | — |

### `data_aggregate_push`

Bulk push aggregate data values via POST /api/dataValueSets.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `data_values` | `list[object]` | yes | — |
| `data_set` | `string` | no | — |
| `period` | `string` | no | — |
| `org_unit` | `string` | no | — |
| `dry_run` | `boolean` | no | — |
| `import_strategy` | `string` | no | — |
| `profile` | `string` | no | — |

### `data_aggregate_set`

Set a single aggregate data value via POST /api/dataValues.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `data_element` | `string` | yes | — |
| `period` | `string` | yes | — |
| `org_unit` | `string` | yes | — |
| `value` | `string` | yes | — |
| `category_option_combo` | `string` | no | — |
| `attribute_option_combo` | `string` | no | — |
| `comment` | `string` | no | — |
| `profile` | `string` | no | — |

### `data_tracker_enrollment_list`

List DHIS2 tracker enrollments.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program` | `string` | no | — |
| `org_unit` | `string` | no | — |
| `ou_mode` | `string` | no | — |
| `tracked_entity` | `string` | no | — |
| `status` | `string` | no | — |
| `fields` | `string` | no | — |
| `page_size` | `integer` | no | — |
| `page` | `integer` | no | — |
| `updated_after` | `string` | no | — |
| `profile` | `string` | no | — |

### `data_tracker_event_list`

List DHIS2 tracker events.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program` | `string` | no | — |
| `program_stage` | `string` | no | — |
| `org_unit` | `string` | no | — |
| `ou_mode` | `string` | no | — |
| `tracked_entity` | `string` | no | — |
| `enrollment` | `string` | no | — |
| `status` | `string` | no | — |
| `occurred_after` | `string` | no | — |
| `occurred_before` | `string` | no | — |
| `fields` | `string` | no | — |
| `page_size` | `integer` | no | — |
| `page` | `integer` | no | — |
| `profile` | `string` | no | — |

### `data_tracker_get`

Fetch one tracked entity by UID (TrackedEntityType inferred from the entity).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `program` | `string` | no | — |
| `fields` | `string` | no | — |
| `profile` | `string` | no | — |

### `data_tracker_list`

List tracked entities of the given TrackedEntityType.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | `string` | yes | — |
| `program` | `string` | no | — |
| `tracked_entities` | `string` | no | — |
| `org_unit` | `string` | no | — |
| `ou_mode` | `string` | no | — |
| `fields` | `string` | no | — |
| `filter` | `string` | no | — |
| `page_size` | `integer` | no | — |
| `page` | `integer` | no | — |
| `updated_after` | `string` | no | — |
| `profile` | `string` | no | — |

### `data_tracker_push`

Bulk import a tracker bundle via POST /api/tracker.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `bundle` | `object` | yes | — |
| `import_strategy` | `string` | no | — |
| `atomic_mode` | `string` | no | — |
| `dry_run` | `boolean` | no | — |
| `async_mode` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `data_tracker_relationship_list`

List DHIS2 relationships (one of tracked_entity/enrollment/event required).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `tracked_entity` | `string` | no | — |
| `enrollment` | `string` | no | — |
| `event` | `string` | no | — |
| `fields` | `string` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `data_tracker_type_list`

List every TrackedEntityType configured on the connected instance.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

## `doctor`

### `doctor_bugs`

Run only BUGS.md workaround drift probes (workspace maintenance).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `doctor_integrity`

Run only DHIS2's `/api/dataIntegrity/summary` probes.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `doctor_metadata`

Run only the workspace metadata-health probes (no DHIS2 integrity, no bug drift).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `doctor_run`

Probe a DHIS2 instance — metadata health + DHIS2 data-integrity by default.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `all_categories` | `boolean` | no | — |
| `profile` | `string` | no | — |

## `maintenance`

### `maintenance_cache_clear`

POST /api/maintenance/cache — clear every server-side cache.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `maintenance_cleanup_soft_deleted`

Hard-remove soft-deleted rows of the given kind.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `target` | `string` | yes | — |
| `profile` | `string` | no | — |

### `maintenance_dataintegrity_checks`

List every built-in data-integrity check definition.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `maintenance_dataintegrity_result`

Read the stored result of a completed data-integrity run (summary or details mode).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `checks` | `list[string]` | no | — |
| `details` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `maintenance_dataintegrity_run`

Kick off a data-integrity run; returns the task envelope.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `checks` | `list[string]` | no | — |
| `details` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `maintenance_task_list`

List every task UID recorded for a given job type (most-recent first).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `task_type` | `string` | yes | — |
| `profile` | `string` | no | — |

### `maintenance_task_status`

Return every notification emitted by a task, oldest first.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `task_type` | `string` | yes | — |
| `task_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `maintenance_task_types`

List every background-job type DHIS2 tracks under /api/system/tasks.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

## `metadata`

### `metadata_diff`

Structurally compare two metadata bundles (or one bundle vs the live instance).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `left_path` | `string` | yes | — |
| `right_path` | `string` | no | — |
| `live` | `boolean` | no | — |
| `ignore_fields` | `list[string]` | no | — |
| `profile` | `string` | no | — |

### `metadata_export`

Download a metadata bundle from `GET /api/metadata`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resources` | `list[string]` | no | — |
| `fields` | `string` | no | — |
| `per_resource_filters` | `object` | no | — |
| `per_resource_fields` | `object` | no | — |
| `skip_sharing` | `boolean` | no | — |
| `skip_translation` | `boolean` | no | — |
| `skip_validation` | `boolean` | no | — |
| `check_references` | `boolean` | no | — |
| `output_path` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_get`

Fetch one metadata object by UID from the named resource.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | yes | — |
| `uid` | `string` | yes | — |
| `fields` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_import`

Upload a metadata bundle via `POST /api/metadata`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `bundle_path` | `string` | no | — |
| `bundle_inline` | `object` | no | — |
| `import_strategy` | `string` | no | — |
| `atomic_mode` | `string` | no | — |
| `dry_run` | `boolean` | no | — |
| `identifier` | `string` | no | — |
| `skip_sharing` | `boolean` | no | — |
| `skip_translation` | `boolean` | no | — |
| `skip_validation` | `boolean` | no | — |
| `merge_mode` | `string` | no | — |
| `preheat_mode` | `string` | no | — |
| `flush_mode` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_list`

List instances of a metadata resource (e.g. `dataElements`, `indicators`).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | yes | — |
| `fields` | `string` | no | — |
| `filters` | `list[string]` | no | — |
| `root_junction` | `string` | no | — |
| `order` | `list[string]` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `paging` | `boolean` | no | — |
| `translate` | `boolean` | no | — |
| `locale` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_patch`

Apply an RFC 6902 JSON Patch to a metadata object.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | yes | — |
| `uid` | `string` | yes | — |
| `ops` | `list[object]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_type_list`

List every metadata resource type the connected DHIS2 instance exposes.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

## `profile`

### `profile_list`

List every DHIS2 profile the server can see.

No parameters.

### `profile_show`

Show a profile with secrets redacted (token/password/client_secret → '***').

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |

### `profile_verify`

Verify one profile by calling /api/system/info and /api/me.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |

### `profile_verify_all`

Verify every known profile. Returns one result per profile.

No parameters.

## `route`

### `route_add`

Create a route via POST /api/routes.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `payload` | `object` | yes | Typed body for `POST /api/routes` + `PUT /api/routes/{uid}`.  DHIS2 accepts (and requires on create) at least `code`, `name`, `url`. `extra="allow"` preserves anything else the server cares about that isn't explicitly typed here.  `auth` is the discriminated `AuthScheme` union — one of five typed variants keyed on `type`. The codegen `spec_patches` module synthesises the Jackson discriminator that upstream DHIS2 omits (BUGS.md #14), so this field is fully typed end-to-end. Callers either build a concrete variant directly (e.g. `HttpBasicAuthScheme(username=..., password=...)`) or pass a raw dict with a `type` key and pydantic routes it to the right subclass. |
| `profile` | `string` | no | — |

### `route_delete`

Delete a route.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `route_get`

Fetch one route by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `fields` | `string` | no | — |
| `profile` | `string` | no | — |

### `route_list`

List DHIS2 integration routes (GET /api/routes).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `fields` | `string` | no | — |
| `profile` | `string` | no | — |

### `route_patch`

Apply a JSON Patch (RFC 6902) to a route.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `patch` | `list[object \| object \| object \| object \| object \| object]` | yes | — |
| `profile` | `string` | no | — |

### `route_run`

Execute a route — DHIS2 proxies the request to the configured target URL.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `method` | `string` | no | — |
| `body` | `-` | no | — |
| `sub_path` | `string` | no | — |
| `profile` | `string` | no | — |

### `route_update`

Replace a route via PUT /api/routes/{uid} (full-object semantics).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `payload` | `object` | yes | Typed body for `POST /api/routes` + `PUT /api/routes/{uid}`.  DHIS2 accepts (and requires on create) at least `code`, `name`, `url`. `extra="allow"` preserves anything else the server cares about that isn't explicitly typed here.  `auth` is the discriminated `AuthScheme` union — one of five typed variants keyed on `type`. The codegen `spec_patches` module synthesises the Jackson discriminator that upstream DHIS2 omits (BUGS.md #14), so this field is fully typed end-to-end. Callers either build a concrete variant directly (e.g. `HttpBasicAuthScheme(username=..., password=...)`) or pass a raw dict with a `type` key and pydantic routes it to the right subclass. |
| `profile` | `string` | no | — |

## `system`

### `system_info`

Return /api/system/info for the given profile (see `system_whoami` for precedence).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `system_whoami`

Return the authenticated DHIS2 user.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

## `user`

### `user_get`

Fetch one user by UID or username.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid_or_username` | `string` | yes | — |
| `fields` | `string` | no | — |
| `profile` | `string` | no | — |

### `user_group_add_member`

Add a user to a user group.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `group_uid` | `string` | yes | — |
| `user_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `user_group_get`

Fetch one user group by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `fields` | `string` | no | — |
| `profile` | `string` | no | — |

### `user_group_list`

List DHIS2 user groups with the metadata query surface.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `fields` | `string` | no | — |
| `filters` | `list[string]` | no | — |
| `order` | `list[string]` | no | — |
| `page_size` | `integer` | no | — |
| `paging` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `user_group_remove_member`

Remove a user from a user group.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `group_uid` | `string` | yes | — |
| `user_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `user_group_sharing_get`

Return the current sharing block for one user group.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `user_invite`

Create a user + dispatch the invitation email (POST /api/users/invite).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | `string` | yes | — |
| `first_name` | `string` | yes | — |
| `surname` | `string` | yes | — |
| `username` | `string` | no | — |
| `user_role_uids` | `list[string]` | no | — |
| `org_unit_uids` | `list[string]` | no | — |
| `profile` | `string` | no | — |

### `user_list`

List DHIS2 users.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `fields` | `string` | no | — |
| `filters` | `list[string]` | no | — |
| `root_junction` | `string` | no | — |
| `order` | `list[string]` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `paging` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `user_me`

Return the authenticated user's `/api/me` payload.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `user_reinvite`

Re-send the invitation email for a pending user.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `user_reset_password`

Trigger DHIS2's password-reset email for a user.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `user_role_add_user`

Grant a user a role.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `role_uid` | `string` | yes | — |
| `user_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `user_role_authorities`

Return the sorted authorities carried by one role.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `user_role_get`

Fetch one user role by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `fields` | `string` | no | — |
| `profile` | `string` | no | — |

### `user_role_list`

List DHIS2 user roles with the metadata query surface.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `fields` | `string` | no | — |
| `filters` | `list[string]` | no | — |
| `order` | `list[string]` | no | — |
| `page_size` | `integer` | no | — |
| `paging` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `user_role_remove_user`

Revoke a user's role.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `role_uid` | `string` | yes | — |
| `user_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

