"""Service layer for the `tracker` plugin — DHIS2 tracker API (/api/tracker/*)."""

from __future__ import annotations

from typing import Any

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


async def list_tracked_entities(
    profile: Profile,
    *,
    program: str | None = None,
    tracked_entity_type: str | None = None,
    tracked_entities: str | None = None,
    org_unit: str | None = None,
    ou_mode: str = "DESCENDANTS",
    fields: str | None = None,
    filter: str | None = None,
    page_size: int = 50,
    page: int | None = None,
    updated_after: str | None = None,
) -> dict[str, Any]:
    """List tracked entities via GET /api/tracker/trackedEntities.

    At minimum, supply one of `program`, `tracked_entity_type`, or
    `tracked_entities` (comma-separated UIDs). `program` must point at a
    tracker program (programType=WITH_REGISTRATION).
    """
    params = {"ouMode": ou_mode, "pageSize": page_size}
    if program is not None:
        params["program"] = program
    if tracked_entity_type is not None:
        params["trackedEntityType"] = tracked_entity_type
    if tracked_entities is not None:
        params["trackedEntities"] = tracked_entities
    if org_unit is not None:
        params["orgUnit"] = org_unit
    if fields is not None:
        params["fields"] = fields
    if filter is not None:
        params["filter"] = filter
    if page is not None:
        params["page"] = page
    if updated_after is not None:
        params["updatedAfter"] = updated_after

    async with open_client(profile) as client:
        return await client.get_raw("/api/tracker/trackedEntities", params=params)


async def get_tracked_entity(
    profile: Profile,
    uid: str,
    *,
    program: str | None = None,
    fields: str | None = None,
) -> dict[str, Any]:
    """Fetch one tracked entity by UID via GET /api/tracker/trackedEntities/{uid}."""
    params: dict[str, Any] = {}
    if program is not None:
        params["program"] = program
    if fields is not None:
        params["fields"] = fields
    async with open_client(profile) as client:
        return await client.get_raw(f"/api/tracker/trackedEntities/{uid}", params=params)


async def list_enrollments(
    profile: Profile,
    *,
    program: str | None = None,
    org_unit: str | None = None,
    ou_mode: str = "DESCENDANTS",
    tracked_entity: str | None = None,
    status: str | None = None,
    fields: str | None = None,
    page_size: int = 50,
    page: int | None = None,
    updated_after: str | None = None,
) -> dict[str, Any]:
    """List enrollments via GET /api/tracker/enrollments (tracker programs only)."""
    params: dict[str, Any] = {"ouMode": ou_mode, "pageSize": page_size}
    if program is not None:
        params["program"] = program
    if org_unit is not None:
        params["orgUnit"] = org_unit
    if tracked_entity is not None:
        params["trackedEntity"] = tracked_entity
    if status is not None:
        params["status"] = status
    if fields is not None:
        params["fields"] = fields
    if page is not None:
        params["page"] = page
    if updated_after is not None:
        params["updatedAfter"] = updated_after

    async with open_client(profile) as client:
        return await client.get_raw("/api/tracker/enrollments", params=params)


async def list_events(
    profile: Profile,
    *,
    program: str | None = None,
    program_stage: str | None = None,
    org_unit: str | None = None,
    ou_mode: str = "DESCENDANTS",
    tracked_entity: str | None = None,
    enrollment: str | None = None,
    status: str | None = None,
    occurred_after: str | None = None,
    occurred_before: str | None = None,
    fields: str | None = None,
    page_size: int = 50,
    page: int | None = None,
) -> dict[str, Any]:
    """List events via GET /api/tracker/events.

    Works with both event programs (no registration) and tracker programs.
    """
    params: dict[str, Any] = {"ouMode": ou_mode, "pageSize": page_size}
    for key, value in (
        ("program", program),
        ("programStage", program_stage),
        ("orgUnit", org_unit),
        ("trackedEntity", tracked_entity),
        ("enrollment", enrollment),
        ("status", status),
        ("occurredAfter", occurred_after),
        ("occurredBefore", occurred_before),
        ("fields", fields),
        ("page", page),
    ):
        if value is not None:
            params[key] = value

    async with open_client(profile) as client:
        return await client.get_raw("/api/tracker/events", params=params)


async def list_relationships(
    profile: Profile,
    *,
    tracked_entity: str | None = None,
    enrollment: str | None = None,
    event: str | None = None,
    fields: str | None = None,
    page_size: int = 50,
) -> dict[str, Any]:
    """List relationships via GET /api/tracker/relationships.

    One of `tracked_entity`, `enrollment`, or `event` is required to scope the
    query (DHIS2 does not support an unscoped relationship listing).
    """
    params: dict[str, Any] = {"pageSize": page_size}
    for key, value in (
        ("trackedEntity", tracked_entity),
        ("enrollment", enrollment),
        ("event", event),
        ("fields", fields),
    ):
        if value is not None:
            params[key] = value
    async with open_client(profile) as client:
        return await client.get_raw("/api/tracker/relationships", params=params)


async def push_tracker(
    profile: Profile,
    bundle: dict[str, Any],
    *,
    import_strategy: str | None = None,
    atomic_mode: str | None = None,
    dry_run: bool = False,
    async_mode: bool = False,
) -> dict[str, Any]:
    """Bulk import via POST /api/tracker with a bundle of tracker objects.

    The `bundle` envelope follows DHIS2's tracker payload shape:
      { "trackedEntities": [...], "enrollments": [...], "events": [...],
        "relationships": [...] }
    Any key may be omitted. `import_strategy` is one of `CREATE`, `UPDATE`,
    `CREATE_AND_UPDATE`, `DELETE`. `atomic_mode` is `ALL` or `OBJECT`.
    `dry_run=True` validates without writing. `async_mode=True` returns a job
    reference immediately.
    """
    params: dict[str, Any] = {}
    if import_strategy is not None:
        params["importStrategy"] = import_strategy
    if atomic_mode is not None:
        params["atomicMode"] = atomic_mode
    if dry_run:
        params["dryRun"] = "true"
    if async_mode:
        params["async"] = "true"

    async with open_client(profile) as client:
        return await client.post_raw("/api/tracker", bundle, params=params)
