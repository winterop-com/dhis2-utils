# Maintenance plugin

`dhis2 maintenance` wraps the DHIS2 server's maintenance surface: background-task polling, cache reset, soft-delete cleanup, and data-integrity checks. Every long-running DHIS2 operation returns a task UID — the `task` sub-tree is the shared polling surface those UIDs feed into.

- CLI: `dhis2 maintenance {task,cache,cleanup,dataintegrity}`
- MCP: `maintenance_{task_types,task_list,task_status,cache_clear,cleanup_soft_deleted,dataintegrity_checks,dataintegrity_run,dataintegrity_result}`
- Models: `Notification`, `DataIntegrityCheck`, `DataIntegrityResult`, `DataIntegrityReport` — all exported from `dhis2_client`.

## Tasks

DHIS2 records every background job under `/api/system/tasks`. Three levels:

| Endpoint | Shape | Surfaces as |
|---|---|---|
| `GET /api/system/tasks` | `{TaskType: {uid: [notifications]}}` | `task types` |
| `GET /api/system/tasks/{type}` | `{uid: [notifications]}` | `task list <type>` |
| `GET /api/system/tasks/{type}/{uid}` | `[Notification]` | `task status <type> <uid>` |

```bash
# Which job types does this instance track?
dhis2 maintenance task types

# Which task UIDs exist for ANALYTICS_TABLE?
dhis2 maintenance task list ANALYTICS_TABLE

# Every notification emitted by one task, oldest first.
dhis2 maintenance task status ANALYTICS_TABLE e1xqWiuxDce

# Stream notifications as they arrive; exits on the first completed=true row.
dhis2 maintenance task watch DATA_INTEGRITY <uid> --interval 1 --timeout 120
```

`Notification` fields: `level` (`INFO`/`WARN`/`ERROR`), `category` (the task type), `message`, `completed`, `time`, `uid`, `id`. DHIS2 returns newest-first; the service reverses to chronological so `task status` reads top-to-bottom with the job.

`task watch` de-duplicates rows by `uid`/`id`/`time` so a long poll doesn't print the same notification twice when DHIS2 returns them repeatedly. Pass `--timeout none` (or `None` via the service API) to wait forever — useful for multi-minute analytics rebuilds.

## Cache

```bash
dhis2 maintenance cache
```

POSTs `/api/maintenance/cache` (204 No Content). Drops every server-side cache — Hibernate session cache, Ehcache, the DHIS2 app-settings cache. Useful after a SQL-level config change so the server re-reads from disk.

## Soft-delete cleanup

`dhis2 data aggregate delete` and `dhis2 data tracker push` with `importStrategy=DELETE` don't actually remove rows — they mark them `deleted=true` so DHIS2 can preserve audit trails. Soft-deleted children block parent-metadata removal (see BUGS.md #2). The cleanup sub-commands hit the dedicated maintenance endpoints to purge each kind:

```bash
dhis2 maintenance cleanup data-values         # POST /api/maintenance/softDeletedDataValueRemoval
dhis2 maintenance cleanup events              # POST /api/maintenance/softDeletedEventRemoval
dhis2 maintenance cleanup enrollments         # POST /api/maintenance/softDeletedEnrollmentRemoval
dhis2 maintenance cleanup tracked-entities    # POST /api/maintenance/softDeletedTrackedEntityRemoval
```

Each POST returns 204 No Content when successful; run in order (entities → enrollments → events → data values) when dismantling a full tracker program.

## Data integrity

DHIS2 ships ~108 data-integrity checks (v42). Each has a stable `name` (query-param value when running it), a `displayName`, `section`, `severity` (`INFO`/`WARNING`/`SEVERE`/`CRITICAL`), `description`, and `recommendation`.

```bash
# Catalog — every built-in check.
dhis2 maintenance dataintegrity list

# Kick off a summary run on one check (or omit for all). Async — returns
# a JobConfigurationWebMessageResponse whose response.id is the task UID.
dhis2 maintenance dataintegrity run orgunits_invalid_geometry

# Same, but populates issues[] per check (heavier; use on specific checks).
dhis2 maintenance dataintegrity run orgunits_invalid_geometry --details

# Read stored results. Summary mode gives per-check `count`; details gives issues[].
dhis2 maintenance dataintegrity result orgunits_invalid_geometry
dhis2 maintenance dataintegrity result orgunits_invalid_geometry --details
```

`run` kicks off the job; `result` reads what the job stored. To follow one run to completion before reading the result:

```bash
TASK_UID="$(dhis2 maintenance dataintegrity run orgunits_invalid_geometry | jq -r '.response.id')"
dhis2 maintenance task watch DATA_INTEGRITY "$TASK_UID" --interval 1 --timeout 60
dhis2 maintenance dataintegrity result orgunits_invalid_geometry
```

DHIS2 uses separate job types for the two modes: `DATA_INTEGRITY` for summary, `DATA_INTEGRITY_DETAILS` for details — pass the right type to `task watch`.

## Library API

Every operation is a plain async function in `dhis2_core.plugins.maintenance.service`:

```python
from dhis2_core.plugins.maintenance import service
from dhis2_core.plugins.maintenance.service import SoftDeleteTarget

await service.list_task_types(profile)
await service.watch_task(profile, "DATA_INTEGRITY", task_uid, interval=1.0)
await service.clear_cache(profile)
await service.remove_soft_deleted(profile, SoftDeleteTarget.DATA_VALUES)
await service.run_dataintegrity(profile, checks=["check_a"], details=False)
report = await service.get_dataintegrity_summary(profile)
```

The `DataIntegrityReport.results: dict[check_name, DataIntegrityResult]` shape mirrors DHIS2's response shape directly — iterate `.results.items()` to render tables or filter by severity.
