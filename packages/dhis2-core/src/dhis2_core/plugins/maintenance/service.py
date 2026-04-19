"""Service layer for the `maintenance` plugin — tasks, cache, cleanup, data-integrity."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Sequence
from enum import StrEnum

from dhis2_client import (
    DataIntegrityCheck,
    DataIntegrityReport,
    Notification,
    WebMessageResponse,
)

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


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
            identifier = notification.uid or notification.id or notification.time or ""
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
        raw = await client.post_raw(path, params=params)
    return WebMessageResponse.model_validate(raw)


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
