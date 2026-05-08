"""Service layer for the `maintenance` plugin — tasks, cache, cleanup, data-integrity, validation, predictors."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Sequence
from enum import StrEnum

from dhis2w_client import (
    DataIntegrityCheck,
    DataIntegrityReport,
    ExpressionContext,
    ExpressionDescription,
    Notification,
    ValidationAnalysisResult,
    WebMessageResponse,
)
from dhis2w_client.generated.v42.oas import ValidationResult

from dhis2w_core.client_context import open_client
from dhis2w_core.profile import Profile


class SoftDeleteTarget(StrEnum):
    """Which kind of soft-deleted row to purge from DHIS2."""

    DATA_VALUES = "data-values"
    EVENTS = "events"
    ENROLLMENTS = "enrollments"
    TRACKED_ENTITIES = "tracked-entities"


_SOFT_DELETE_ENDPOINT: dict[SoftDeleteTarget, str] = {
    SoftDeleteTarget.DATA_VALUES: "/api/maintenance/softDeletedDataValueRemoval",
    SoftDeleteTarget.EVENTS: "/api/maintenance/softDeletedEventRemoval",
    SoftDeleteTarget.ENROLLMENTS: "/api/maintenance/softDeletedEnrollmentRemoval",
    SoftDeleteTarget.TRACKED_ENTITIES: "/api/maintenance/softDeletedTrackedEntityRemoval",
}


async def list_task_types(profile: Profile) -> list[str]:
    """Return every background-job type DHIS2 tracks under `/api/system/tasks`.

    The endpoint returns `{TaskType: {uid: [notifications]}}`; we surface
    just the sorted type names.
    """
    async with open_client(profile) as client:
        raw = await client.get_raw("/api/system/tasks")
    return sorted(raw.keys())


async def list_task_ids(profile: Profile, task_type: str) -> list[str]:
    """Return every task UID recorded for a given job type.

    The endpoint returns `{uid: [notifications]}`; we surface just the
    UIDs, sorted so repeated runs are stable.
    """
    async with open_client(profile) as client:
        raw = await client.get_raw(f"/api/system/tasks/{task_type}")
    return sorted(raw.keys())


async def get_task_notifications(profile: Profile, task_type: str, task_uid: str) -> list[Notification]:
    """Fetch the full notifier feed for one task (oldest first after reversing DHIS2's order).

    DHIS2 returns notifications newest-first; we reverse so callers reading
    top-to-bottom follow the job chronologically. A `completed=true` row with
    `level` in (`INFO`, `WARN`, `ERROR`) marks the terminal state.
    """
    async with open_client(profile) as client:
        raw = await client.get_raw(f"/api/system/tasks/{task_type}/{task_uid}")
    items = [Notification.model_validate(item) for item in _unwrap_list(raw)]
    return list(reversed(items))


def _unwrap_list(raw: object) -> list[object]:
    """Pull the list out of `_parse_json`'s `{"data": [...]}` wrapper."""
    if isinstance(raw, dict) and "data" in raw:
        data = raw["data"]
        return list(data) if isinstance(data, list) else []
    return []


async def watch_task(
    profile: Profile,
    task_type: str,
    task_uid: str,
    *,
    interval: float = 2.0,
    timeout: float | None = 600.0,
) -> AsyncIterator[Notification]:
    """Poll `/api/system/tasks/{type}/{uid}` until the job completes.

    Yields each new notification as it arrives. Exits when any row reports
    `completed=true`; raises `TimeoutError` if `timeout` seconds elapse first.
    Pass `timeout=None` to wait forever (useful for analytics-table rebuilds).
    """
    deadline = None if timeout is None else asyncio.get_event_loop().time() + timeout
    seen: set[str] = set()
    while True:
        notifications = await get_task_notifications(profile, task_type, task_uid)
        for notification in notifications:
            identifier = (
                notification.uid
                or notification.id
                or (notification.time.isoformat() if notification.time is not None else "")
            )
            if identifier and identifier in seen:
                continue
            if identifier:
                seen.add(identifier)
            yield notification
            if notification.completed:
                return
        if deadline is not None and asyncio.get_event_loop().time() >= deadline:
            raise TimeoutError(f"task {task_type}/{task_uid} did not complete within {timeout}s")
        await asyncio.sleep(interval)


async def clear_cache(profile: Profile) -> None:
    """POST /api/maintenance/cache — drop every Hibernate + app cache server-side."""
    async with open_client(profile) as client:
        await client.post_raw("/api/maintenance/cache")


async def remove_soft_deleted(profile: Profile, target: SoftDeleteTarget) -> None:
    """Hard-delete rows that were soft-deleted by a prior DELETE import.

    DHIS2 keeps soft-deleted rows so audit trails stay intact, but those rows
    block parent-metadata removal (see BUGS.md #2). This endpoint purges them.
    """
    endpoint = _SOFT_DELETE_ENDPOINT[target]
    async with open_client(profile) as client:
        await client.post_raw(endpoint)


async def list_dataintegrity_checks(profile: Profile) -> list[DataIntegrityCheck]:
    """GET /api/dataIntegrity — every built-in check + its severity + recommendation."""
    async with open_client(profile) as client:
        raw = await client.get_raw("/api/dataIntegrity")
    return [DataIntegrityCheck.model_validate(item) for item in _unwrap_list(raw)]


async def run_dataintegrity(
    profile: Profile,
    *,
    checks: Sequence[str] | None = None,
    details: bool = False,
) -> WebMessageResponse:
    """Kick off a data-integrity run asynchronously; returns the task envelope.

    `checks` is the list of check `name`s (from `list_dataintegrity_checks`);
    omit to run every check. `details=True` hits `/api/dataIntegrity/details`
    (populates `issues[]`); the default `False` hits `/api/dataIntegrity`
    (summary — just `count`). Poll progress with
    `watch_task(profile, "DATA_INTEGRITY" | "DATA_INTEGRITY_DETAILS", task_uid)`.
    """
    path = "/api/dataIntegrity/details" if details else "/api/dataIntegrity"
    params: dict[str, list[str]] = {}
    if checks:
        params["checks"] = list(checks)
    async with open_client(profile) as client:
        return await client.post(path, body=None, params=params, model=WebMessageResponse)


async def get_dataintegrity_summary(profile: Profile, *, checks: Sequence[str] | None = None) -> DataIntegrityReport:
    """GET /api/dataIntegrity/summary — per-check `count` + timing after a run."""
    params: dict[str, list[str]] = {}
    if checks:
        params["checks"] = list(checks)
    async with open_client(profile) as client:
        raw = await client.get_raw("/api/dataIntegrity/summary", params=params)
    return DataIntegrityReport.from_api(raw)


async def get_dataintegrity_details(profile: Profile, *, checks: Sequence[str] | None = None) -> DataIntegrityReport:
    """GET /api/dataIntegrity/details — per-check `issues[]` (offending rows)."""
    params: dict[str, list[str]] = {}
    if checks:
        params["checks"] = list(checks)
    async with open_client(profile) as client:
        raw = await client.get_raw("/api/dataIntegrity/details", params=params)
    return DataIntegrityReport.from_api(raw)


async def refresh_analytics(
    profile: Profile,
    *,
    skip_resource_tables: bool = False,
    last_years: int | None = None,
) -> WebMessageResponse:
    """Trigger analytics-table regeneration via POST /api/resourceTables/analytics.

    Returns a typed `JobConfigurationWebMessageResponse` envelope wrapped by
    `WebMessageResponse`. Use `.task_ref()` to get the `(ANALYTICS_TABLE,
    task_uid)` tuple + pass it to `client.tasks.await_completion` to
    block until done.
    """
    params: dict[str, str | int] = {}
    if skip_resource_tables:
        params["skipResourceTables"] = "true"
    if last_years is not None:
        params["lastYears"] = last_years
    async with open_client(profile) as client:
        return await client.post(
            "/api/resourceTables/analytics",
            body=None,
            params=params,
            model=WebMessageResponse,
        )


async def refresh_resource_tables(profile: Profile) -> WebMessageResponse:
    """Trigger resource-table regeneration via POST /api/resourceTables.

    DHIS2 distinguishes analytics tables (the full star-schema fact + dim
    tables, rebuilt by `refresh_analytics`) from resource tables (supporting
    OU / category hierarchies). Most analytics workflows want
    `refresh_analytics` — it also refreshes resource tables unless
    `skip_resource_tables=True`. This endpoint regenerates ONLY the
    resource tables without touching the analytics star schema. Job type
    is `RESOURCE_TABLE`.
    """
    async with open_client(profile) as client:
        return await client.post("/api/resourceTables", body=None, model=WebMessageResponse)


async def refresh_monitoring(profile: Profile) -> WebMessageResponse:
    """Trigger monitoring-table regeneration via POST /api/resourceTables/monitoring.

    Rebuilds the tables backing DHIS2's data-quality / validation-rule
    monitoring. Independent of the analytics + resource tables. Job type
    is `MONITORING`.
    """
    async with open_client(profile) as client:
        return await client.post("/api/resourceTables/monitoring", body=None, model=WebMessageResponse)


# ---- validation-rule workflow -------------------------------------------------


async def run_validation_analysis(
    profile: Profile,
    *,
    org_unit: str,
    start_date: str,
    end_date: str,
    validation_rule_group: str | None = None,
    max_results: int | None = None,
    notification: bool = False,
    persist: bool = False,
) -> list[ValidationAnalysisResult]:
    """Run a synchronous validation-rule analysis + return violations."""
    async with open_client(profile) as client:
        return await client.validation.run_analysis(
            org_unit=org_unit,
            start_date=start_date,
            end_date=end_date,
            validation_rule_group=validation_rule_group,
            max_results=max_results,
            notification=notification,
            persist=persist,
        )


async def list_validation_results(
    profile: Profile,
    *,
    org_unit: str | None = None,
    period: str | None = None,
    validation_rule: str | None = None,
    created_date: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
) -> list[ValidationResult]:
    """List persisted validation results."""
    async with open_client(profile) as client:
        return await client.validation.list_results(
            org_unit=org_unit,
            period=period,
            validation_rule=validation_rule,
            created_date=created_date,
            page=page,
            page_size=page_size,
        )


async def get_validation_result(profile: Profile, result_id: int | str) -> ValidationResult:
    """Fetch a single persisted validation result by its numeric id."""
    async with open_client(profile) as client:
        return await client.validation.get_result(result_id)


async def delete_validation_results(
    profile: Profile,
    *,
    org_units: Sequence[str] | None = None,
    periods: Sequence[str] | None = None,
    validation_rules: Sequence[str] | None = None,
) -> None:
    """Bulk-delete validation results matching the filters."""
    async with open_client(profile) as client:
        await client.validation.delete_results(
            org_units=org_units,
            periods=periods,
            validation_rules=validation_rules,
        )


async def send_validation_notifications(profile: Profile) -> WebMessageResponse:
    """Fire configured notification templates for every current validation violation."""
    async with open_client(profile) as client:
        return await client.validation.send_notifications()


async def describe_expression(
    profile: Profile,
    expression: str,
    *,
    context: ExpressionContext = "generic",
) -> ExpressionDescription:
    """Parse-check an expression + render a human description."""
    async with open_client(profile) as client:
        return await client.validation.describe_expression(expression, context=context)


# ---- predictors workflow ----------------------------------------------------


async def run_predictors(
    profile: Profile,
    *,
    start_date: str,
    end_date: str,
    predictor_uid: str | None = None,
    group_uid: str | None = None,
) -> WebMessageResponse:
    """Run predictor expressions + emit data values.

    Pass `predictor_uid` to run one predictor, `group_uid` for a group, or
    neither to run every predictor on the instance. `start_date` / `end_date`
    bound the periods predictions are generated for.
    """
    if predictor_uid and group_uid:
        raise ValueError("run_predictors: pass at most one of predictor_uid / group_uid")
    async with open_client(profile) as client:
        if predictor_uid is not None:
            return await client.predictors.run_one(
                predictor_uid,
                start_date=start_date,
                end_date=end_date,
            )
        if group_uid is not None:
            return await client.predictors.run_group(
                group_uid,
                start_date=start_date,
                end_date=end_date,
            )
        return await client.predictors.run_all(start_date=start_date, end_date=end_date)
