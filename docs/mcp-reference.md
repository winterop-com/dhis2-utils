# MCP reference

Every tool exposed by the `dhis2` FastMCP server, grouped by plugin. Auto-generated from the in-process server — do not edit by hand. Rebuild via `make docs-mcp` (chained into `make docs-build`).

**Total tools**: 224 across 13 plugin groups.

## Plugins

- [`analytics_*`](#analytics) — 5 tools
- [`apps_*`](#apps) — 13 tools
- [`customize_*`](#customize) — 7 tools
- [`data_*`](#data) — 15 tools
- [`doctor_*`](#doctor) — 4 tools
- [`files_*`](#files) — 5 tools
- [`maintenance_*`](#maintenance) — 15 tools
- [`messaging_*`](#messaging) — 11 tools
- [`metadata_*`](#metadata) — 120 tools
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

## `apps`

### `apps_get`

Return one installed app by `key`; None if not installed.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | yes | — |
| `profile` | `string` | no | — |

### `apps_hub_list`

List apps available in the configured App Hub (`GET /api/appHub`).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | `string` | no | — |
| `profile` | `string` | no | — |

### `apps_hub_url_get`

Read DHIS2's configured App Hub URL (`keyAppHubUrl` system setting).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `apps_hub_url_set`

Point DHIS2 at a different App Hub by writing the `keyAppHubUrl` system setting.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | `string` | yes | — |
| `profile` | `string` | no | — |

### `apps_install_from_file`

Install / update an app from a local `.zip` at `path` (`POST /api/apps`).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | yes | — |
| `profile` | `string` | no | — |

### `apps_install_from_hub`

Install an App Hub version (`POST /api/appHub/{versionId}`).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `version_id` | `string` | yes | — |
| `profile` | `string` | no | — |

### `apps_list`

List every installed DHIS2 app (`GET /api/apps`). Returns typed App records.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `apps_reload`

Re-read every app from disk (`PUT /api/apps`). No new versions fetched.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `apps_restore`

Reinstall every hub-backed entry in the given snapshot.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `snapshot` | `object` | yes | Typed inventory of every installed app — portable across instances. |
| `dry_run` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `apps_snapshot`

Capture a portable inventory of every installed app.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `apps_uninstall`

Remove an installed app by `key` (`DELETE /api/apps/{key}`).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | yes | — |
| `profile` | `string` | no | — |

### `apps_update`

Update a single installed app to its latest App Hub version.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | yes | — |
| `dry_run` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `apps_update_all`

Walk every installed app; install the latest App Hub version where available.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dry_run` | `boolean` | no | — |
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

### `data_tracker_enroll`

Add an enrollment to an existing tracked entity.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `tracked_entity` | `string` | yes | — |
| `program` | `string` | yes | — |
| `org_unit` | `string` | yes | — |
| `enrolled_at` | `string` | no | — |
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

### `data_tracker_event_create`

Add one event — tracker (with enrollment) or event-only (standalone).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program` | `string` | yes | — |
| `program_stage` | `string` | yes | — |
| `org_unit` | `string` | yes | — |
| `enrollment` | `string` | no | — |
| `tracked_entity` | `string` | no | — |
| `data_values` | `object` | no | — |
| `occurred_at` | `string` | no | — |
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

### `data_tracker_outstanding`

List ACTIVE enrollments missing events on any non-repeatable stage.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program` | `string` | yes | — |
| `org_unit` | `string` | no | — |
| `ou_mode` | `string` | no | — |
| `page_size` | `integer` | no | — |
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

### `data_tracker_register`

Register a tracked entity + enroll in one program via POST /api/tracker.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program` | `string` | yes | — |
| `org_unit` | `string` | yes | — |
| `tracked_entity_type` | `string` | yes | — |
| `attributes` | `object` | no | — |
| `enrolled_at` | `string` | no | — |
| `events` | `list[object]` | no | — |
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

## `files`

### `files_documents_create_external`

Create an EXTERNAL_URL document — no bytes uploaded, DHIS2 links out to `url`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `url` | `string` | yes | — |
| `profile` | `string` | no | — |

### `files_documents_delete`

Delete one document by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `files_documents_get`

Return typed metadata for one document by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `files_documents_list`

List DHIS2 documents (`/api/documents`).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `filter` | `string` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `files_resources_get`

Return typed metadata for one file resource (`/api/fileResources/{uid}`).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
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

### `maintenance_predictors_run`

Run predictor expressions + emit data values.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `start_date` | `string` | yes | — |
| `end_date` | `string` | yes | — |
| `predictor_uid` | `string` | no | — |
| `group_uid` | `string` | no | — |
| `profile` | `string` | no | — |

### `maintenance_refresh_analytics`

Regenerate the analytics star schema (POST /api/resourceTables/analytics, job=ANALYTICS_TABLE).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `skip_resource_tables` | `boolean` | no | — |
| `last_years` | `integer` | no | — |
| `profile` | `string` | no | — |

### `maintenance_refresh_monitoring`

Regenerate monitoring tables (POST /api/resourceTables/monitoring, job=MONITORING).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `maintenance_refresh_resource_tables`

Regenerate resource tables only (POST /api/resourceTables, job=RESOURCE_TABLE).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
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

### `maintenance_validation_result_list`

List persisted validation results, with optional filters.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `org_unit` | `string` | no | — |
| `period` | `string` | no | — |
| `validation_rule` | `string` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `maintenance_validation_run`

Run a validation-rule analysis synchronously + return violations.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `org_unit` | `string` | yes | — |
| `start_date` | `string` | yes | — |
| `end_date` | `string` | yes | — |
| `validation_rule_group` | `string` | no | — |
| `max_results` | `integer` | no | — |
| `notification` | `boolean` | no | — |
| `persist` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `maintenance_validation_validate_expression`

Parse-check a DHIS2 expression + render a human description.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `expression` | `string` | yes | — |
| `context` | `string` | no | — |
| `profile` | `string` | no | — |

## `messaging`

### `messaging_assign`

Assign a conversation to a user (ticket workflows).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `user_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `messaging_delete`

Delete a conversation (soft-delete for the calling user).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `messaging_get`

Fetch one conversation with its full message thread.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `messaging_list`

List conversations the authenticated user is part of.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `filter` | `string` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `messaging_mark_read`

Mark one or more conversations as read.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `messaging_mark_unread`

Mark one or more conversations as unread.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `messaging_reply`

Reply to an existing conversation with a plain-text message.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `text` | `string` | yes | — |
| `profile` | `string` | no | — |

### `messaging_send`

Create a new conversation with an initial message; returns the typed conversation.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `subject` | `string` | yes | — |
| `text` | `string` | yes | — |
| `users` | `list[string]` | no | — |
| `user_groups` | `list[string]` | no | — |
| `organisation_units` | `list[string]` | no | — |
| `attachments` | `list[string]` | no | — |
| `profile` | `string` | no | — |

### `messaging_set_priority`

Set a conversation's ticket-workflow priority: NONE / LOW / MEDIUM / HIGH.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `priority` | `string` | yes | — |
| `profile` | `string` | no | — |

### `messaging_set_status`

Set a conversation's ticket-workflow status: NONE / OPEN / PENDING / INVALID / SOLVED.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `status` | `string` | yes | — |
| `profile` | `string` | no | — |

### `messaging_unassign`

Remove the assignee from a conversation.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

## `metadata`

### `metadata_attribute_delete`

Remove one attribute value; True if anything was removed, False on no-op.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | yes | — |
| `resource_uid` | `string` | yes | — |
| `attribute` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_attribute_find`

Reverse lookup — UIDs of every resource whose attribute value matches.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | yes | — |
| `attribute` | `string` | yes | — |
| `value` | `string` | yes | — |
| `extra_filters` | `list[string]` | no | — |
| `profile` | `string` | no | — |

### `metadata_attribute_get`

Read one attribute value off any resource with `attributeValues`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | yes | — |
| `resource_uid` | `string` | yes | — |
| `attribute` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_attribute_set`

Set / replace one attribute value on any resource (read-merge-write).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | yes | — |
| `resource_uid` | `string` | yes | — |
| `attribute` | `string` | yes | — |
| `value` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_dashboard_add_item`

Add one metadata-backed item to a dashboard.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dashboard_uid` | `string` | yes | — |
| `target_uid` | `string` | yes | — |
| `kind` | `string` | no | — |
| `x` | `integer` | no | — |
| `y` | `integer` | no | — |
| `width` | `integer` | no | — |
| `height` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_dashboard_list`

List every Dashboard on the instance, sorted by name.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_dashboard_show`

Show one Dashboard with every dashboardItem resolved inline.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `dashboard_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_create`

Create a DataElement. Omit `category_combo_uid` to use the instance default.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `value_type` | `string` | yes | — |
| `domain_type` | `string` | no | — |
| `aggregation_type` | `string` | no | — |
| `category_combo_uid` | `string` | no | — |
| `option_set_uid` | `string` | no | — |
| `legend_set_uids` | `list[string]` | no | — |
| `code` | `string` | no | — |
| `form_name` | `string` | no | — |
| `description` | `string` | no | — |
| `uid` | `string` | no | — |
| `zero_is_significant` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `metadata_data_element_delete`

Delete a DataElement — DHIS2 rejects deletes on DEs with saved values.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_add_members`

Add DataElements to a group via the per-item POST shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `data_element_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_create`

Create an empty DataElementGroup.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `uid` | `string` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_delete`

Delete a DataElementGroup — members stay.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_list`

List every DataElementGroup.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_data_element_group_members`

Page through DataElements in a group.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_remove_members`

Drop DataElements from a group via the per-item DELETE shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `data_element_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_set_add_groups`

Add groups to a group set via the per-item POST shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `group_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_set_create`

Create an empty DataElementGroupSet.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `uid` | `string` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `compulsory` | `boolean` | no | — |
| `data_dimension` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_set_delete`

Delete a DataElementGroupSet — groups stay.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_set_list`

List every DataElementGroupSet.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_data_element_group_set_remove_groups`

Drop groups from a group set via the per-item DELETE shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `group_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_set_show`

Fetch one DataElementGroupSet by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_group_show`

Fetch one DataElementGroup with member + group-set refs inline.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_list`

Page through DataElements. `domain_type` = `AGGREGATE` or `TRACKER`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `domain_type` | `string` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_data_element_rename`

Partial-update the label fields on a DataElement.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `name` | `string` | no | — |
| `short_name` | `string` | no | — |
| `form_name` | `string` | no | — |
| `description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_data_element_set_legend_sets`

Replace the legend-set refs on a DataElement (empty list clears).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `legend_set_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_data_element_show`

Fetch one DataElement by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_diff`

Structurally compare two metadata bundles (or one bundle vs the live instance).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `left_path` | `string` | yes | — |
| `right_path` | `string` | no | — |
| `live` | `boolean` | no | — |
| `ignore_fields` | `list[string]` | no | — |
| `profile` | `string` | no | — |

### `metadata_diff_profiles`

Diff a narrow metadata slice between two registered profiles.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile_a` | `string` | yes | — |
| `profile_b` | `string` | yes | — |
| `resources` | `list[string]` | yes | — |
| `per_resource_filters` | `object` | no | — |
| `fields` | `string` | no | — |
| `ignore_fields` | `list[string]` | no | — |

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

### `metadata_indicator_create`

Create an Indicator from numerator / denominator expressions.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `indicator_type_uid` | `string` | yes | — |
| `numerator` | `string` | yes | — |
| `denominator` | `string` | yes | — |
| `numerator_description` | `string` | no | — |
| `denominator_description` | `string` | no | — |
| `legend_set_uids` | `list[string]` | no | — |
| `annualized` | `boolean` | no | — |
| `decimals` | `integer` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `uid` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_indicator_delete`

Delete an Indicator.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_add_members`

Add Indicators to a group via the per-item POST shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `indicator_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_create`

Create an empty IndicatorGroup.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `uid` | `string` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_delete`

Delete an IndicatorGroup — members stay.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_list`

List every IndicatorGroup.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_indicator_group_members`

Page through Indicators in a group.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_remove_members`

Drop Indicators from a group via the per-item DELETE shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `indicator_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_set_add_groups`

Add groups to an IndicatorGroupSet via the per-item POST shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `group_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_set_create`

Create an empty IndicatorGroupSet.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `uid` | `string` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `compulsory` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_set_delete`

Delete an IndicatorGroupSet — groups stay.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_set_list`

List every IndicatorGroupSet.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_indicator_group_set_remove_groups`

Drop groups from an IndicatorGroupSet via the per-item DELETE shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `group_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_set_show`

Fetch one IndicatorGroupSet by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_group_show`

Fetch one IndicatorGroup with member + group-set refs.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_list`

Page through Indicators.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_indicator_rename`

Partial-update the label fields on an Indicator.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `name` | `string` | no | — |
| `short_name` | `string` | no | — |
| `description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_indicator_set_legend_sets`

Replace the legend-set refs on an Indicator.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `legend_set_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_show`

Fetch one Indicator by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_indicator_validate_expression`

Parse-check one numerator / denominator expression via DHIS2's validator.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `expression` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_legend_set_create`

Create a LegendSet with ordered colour-range legends.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `legends` | `list[object]` | yes | — |
| `code` | `string` | no | — |
| `uid` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_legend_set_delete`

Delete a LegendSet by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_legend_set_list`

List every LegendSet with its `legends` child bands resolved inline.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_legend_set_show`

Fetch one LegendSet by UID with its colour bands resolved inline.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
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

### `metadata_map_clone`

Clone an existing Map with a fresh UID + new name.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `source_uid` | `string` | yes | — |
| `new_name` | `string` | yes | — |
| `new_uid` | `string` | no | — |
| `new_description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_map_create`

Create a single-layer thematic choropleth Map.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `data_elements` | `list[string]` | yes | — |
| `periods` | `list[string]` | yes | — |
| `organisation_units` | `list[string]` | yes | — |
| `organisation_unit_levels` | `list[integer]` | yes | — |
| `description` | `string` | no | — |
| `uid` | `string` | no | — |
| `longitude` | `number` | no | — |
| `latitude` | `number` | no | — |
| `zoom` | `integer` | no | — |
| `basemap` | `string` | no | — |
| `classes` | `integer` | no | — |
| `color_low` | `string` | no | — |
| `color_high` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_map_list`

List every Map on the instance, sorted by name.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_map_show`

Show one Map with its viewport + every mapViews layer resolved inline.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `map_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_merge`

Export a metadata slice from one profile and import it into another.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `source_profile` | `string` | yes | — |
| `target_profile` | `string` | yes | — |
| `resources` | `list[string]` | yes | — |
| `per_resource_filters` | `object` | no | — |
| `fields` | `string` | no | — |
| `strategy` | `string` | no | — |
| `atomic` | `string` | no | — |
| `include_sharing` | `boolean` | no | — |
| `dry_run` | `boolean` | no | — |

### `metadata_options_attribute_find`

Reverse lookup — find the Option in a set whose attribute matches a value.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `set_ref` | `string` | yes | — |
| `attribute` | `string` | yes | — |
| `value` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_options_attribute_get`

Read one attribute value off an Option; None if unset.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `option_uid` | `string` | yes | — |
| `attribute` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_options_attribute_set`

Set / replace one attribute value on an Option (read-merge-write).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `option_uid` | `string` | yes | — |
| `attribute` | `string` | yes | — |
| `value` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_options_find`

Locate one option in a set by `option_code` or `option_name`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `set_ref` | `string` | yes | — |
| `option_code` | `string` | no | — |
| `option_name` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_options_show`

Fetch one OptionSet (with options inline) by UID or business code.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid_or_code` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_options_sync`

Idempotent bulk sync — reconcile an OptionSet against a spec.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `set_ref` | `string` | yes | — |
| `spec` | `list[object]` | yes | — |
| `remove_missing` | `boolean` | no | — |
| `dry_run` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_create`

Create a child OU under `parent_uid`. `opening_date` is ISO-8601.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `parent_uid` | `string` | yes | — |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `opening_date` | `string` | yes | — |
| `uid` | `string` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_delete`

Delete an OU — DHIS2 rejects deletes on units with children or data.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_add_members`

Add OUs to a group via the per-item POST shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `ou_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_create`

Create an empty OrganisationUnitGroup.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `uid` | `string` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `color` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_delete`

Delete an OrganisationUnitGroup — members stay.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_list`

List every OrganisationUnitGroup.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_members`

Page through OUs that belong to one group.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_remove_members`

Drop OUs from a group via the per-item DELETE shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `ou_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_set_add_groups`

Add groups to a group set via the per-item POST shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `group_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_set_create`

Create an empty OrganisationUnitGroupSet.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `uid` | `string` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `compulsory` | `boolean` | no | — |
| `data_dimension` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_set_delete`

Delete an OrganisationUnitGroupSet — groups stay.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_set_list`

List every OrganisationUnitGroupSet.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_set_remove_groups`

Drop groups from a group set via the per-item DELETE shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `group_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_set_show`

Fetch one group set with per-group member counts.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_group_show`

Fetch one OrganisationUnitGroup with member + group-set refs inline.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_level_list`

List every OrganisationUnitLevel sorted by depth (1 = roots).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_level_rename`

Rename a level row — pass `uid` or `level` (numeric depth), not both.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `uid` | `string` | no | — |
| `level` | `integer` | no | — |
| `code` | `string` | no | — |
| `offline_levels` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_level_show`

Fetch one level row — pass `uid` or `level` (numeric depth), not both.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | no | — |
| `level` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_list`

Page through OrganisationUnits with parent + hierarchy columns.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `level` | `integer` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_move`

Reparent an OU. DHIS2 recomputes `path` + `hierarchyLevel` server-side.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `new_parent_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_show`

Fetch one OrganisationUnit by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_organisation_unit_tree`

Walk a subtree rooted at `root_uid` at bounded depth.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `root_uid` | `string` | yes | — |
| `max_depth` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_patch`

Apply an RFC 6902 JSON Patch to a metadata object.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | yes | — |
| `uid` | `string` | yes | — |
| `ops` | `list[object]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_create`

Create a ProgramIndicator for a given program.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `program_uid` | `string` | yes | — |
| `expression` | `string` | yes | — |
| `analytics_type` | `string` | no | — |
| `filter_expression` | `string` | no | — |
| `description` | `string` | no | — |
| `aggregation_type` | `string` | no | — |
| `decimals` | `integer` | no | — |
| `legend_set_uids` | `list[string]` | no | — |
| `code` | `string` | no | — |
| `uid` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_delete`

Delete a ProgramIndicator.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_group_add_members`

Add ProgramIndicators to a group via the per-item POST shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `program_indicator_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_group_create`

Create an empty ProgramIndicatorGroup.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `short_name` | `string` | yes | — |
| `uid` | `string` | no | — |
| `code` | `string` | no | — |
| `description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_group_delete`

Delete a ProgramIndicatorGroup — members stay.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_group_list`

List every ProgramIndicatorGroup.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_program_indicator_group_members`

Page through ProgramIndicators in a group.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_group_remove_members`

Drop ProgramIndicators from a group via the per-item DELETE shortcut.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `program_indicator_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_group_show`

Fetch one ProgramIndicatorGroup with member refs.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_list`

Page through ProgramIndicators, optionally scoped to one program.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program_uid` | `string` | no | — |
| `page` | `integer` | no | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_rename`

Partial-update the label fields on a ProgramIndicator.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `name` | `string` | no | — |
| `short_name` | `string` | no | — |
| `description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_set_legend_sets`

Replace the legend-set refs on a ProgramIndicator.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `legend_set_uids` | `list[string]` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_show`

Fetch one ProgramIndicator by UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_indicator_validate_expression`

Parse-check one program-indicator expression via DHIS2's validator.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `expression` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_rule_list`

List every ProgramRule (optionally scoped to a program), sorted by priority.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program_uid` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_program_rule_show`

Show one ProgramRule with actions resolved inline.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `rule_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_rule_validate_expression`

Parse-check a program-rule condition expression.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `expression` | `string` | yes | — |
| `context` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_program_rule_vars_for`

List every `ProgramRuleVariable` in scope for a program.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `program_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_program_rule_where_de_is_used`

Impact analysis — every ProgramRule whose actions reference this DataElement.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `data_element_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_search`

Cross-resource text search via `/api/metadata` on id / code / name.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | `string` | yes | — |
| `page_size` | `integer` | no | — |
| `resource` | `string` | no | — |
| `fields` | `string` | no | — |
| `exact` | `boolean` | no | — |
| `profile` | `string` | no | — |

### `metadata_sql_view_execute`

Execute a SqlView and return its result grid as a JSON-friendly payload.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `view_uid` | `string` | yes | — |
| `variables` | `object` | no | — |
| `criteria` | `object` | no | — |
| `profile` | `string` | no | — |

### `metadata_sql_view_list`

List every SqlView on the instance (optionally filtered by `view_type`).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `view_type` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_sql_view_refresh`

Refresh a MATERIALIZED_VIEW or lazily create a VIEW's DB object.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `view_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_sql_view_show`

Show one SqlView with its stored sqlQuery.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `view_uid` | `string` | yes | — |
| `profile` | `string` | no | — |

### `metadata_type_list`

List every metadata resource type the connected DHIS2 instance exposes.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `profile` | `string` | no | — |

### `metadata_usage`

Reverse lookup — find every object that references the given UID.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `uid` | `string` | yes | — |
| `page_size` | `integer` | no | — |
| `profile` | `string` | no | — |

### `metadata_viz_clone`

Clone an existing Visualization with a fresh UID + new name.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `source_uid` | `string` | yes | — |
| `new_name` | `string` | yes | — |
| `new_uid` | `string` | no | — |
| `new_description` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_viz_create`

Create a Visualization from a typed VisualizationSpec.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | yes | — |
| `viz_type` | `string` | yes | — |
| `data_elements` | `list[string]` | yes | — |
| `periods` | `list[string]` | yes | — |
| `organisation_units` | `list[string]` | yes | — |
| `description` | `string` | no | — |
| `uid` | `string` | no | — |
| `category_dimension` | `string` | no | — |
| `series_dimension` | `string` | no | — |
| `filter_dimension` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_viz_list`

List every Visualization on the instance (optionally filtered by type).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `viz_type` | `string` | no | — |
| `profile` | `string` | no | — |

### `metadata_viz_show`

Show one Visualization with axes + data dimensions resolved inline.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `viz_uid` | `string` | yes | — |
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

