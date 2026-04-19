"""Service layer for the `tracker` plugin — DHIS2 tracker API (/api/tracker/*).

Read paths return typed pydantic models from `dhis2_client.generated.v42.tracker`:

  list_tracked_entities   -> list[TrackerTrackedEntity]
  get_tracked_entity      -> TrackerTrackedEntity
  list_enrollments        -> list[TrackerEnrollment]
  list_events             -> list[TrackerEvent]
  list_relationships      -> list[TrackerRelationship]

DHIS2 wraps each list in a domain envelope (`{pager, events: [...]}` etc.) —
the service unwraps it and returns the flat typed list. Callers that need
the `pager` block can call `list_raw` variants (not implemented yet).

Write paths return the typed `WebMessageResponse` envelope.
"""

from __future__ import annotations

import re
from typing import Any

from dhis2_client import WebMessageResponse
from dhis2_client.generated.v42.tracker import (
    TrackerEnrollment,
    TrackerEvent,
    TrackerRelationship,
    TrackerTrackedEntity,
)
from pydantic import BaseModel, ConfigDict

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile

_DHIS2_UID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]{10}$")


async def resolve_tracked_entity_type(profile: Profile, name_or_uid: str) -> str:
    """Return the TrackedEntityType UID for a name or UID.

    If `name_or_uid` matches DHIS2's UID pattern (`[A-Za-z][A-Za-z0-9]{10}`)
    it's returned as-is. Otherwise the value is treated as a case-insensitive
    name + queried via `/api/trackedEntityTypes?filter=name:ilike:...&fields=id`.

    Raises `ValueError` if no matching type is found, or the name is ambiguous.
    """
    if _DHIS2_UID_RE.match(name_or_uid):
        return name_or_uid
    async with open_client(profile) as client:
        response = await client.get_raw(
            "/api/trackedEntityTypes",
            params={"filter": f"name:ilike:{name_or_uid}", "fields": "id,name"},
        )
    matches = response.get("trackedEntityTypes", [])
    if not matches:
        raise ValueError(
            f"no TrackedEntityType matches name {name_or_uid!r} — run `dhis2 data tracker type` to see configured types"
        )
    if len(matches) > 1:
        names = [m.get("name") for m in matches]
        raise ValueError(f"name {name_or_uid!r} is ambiguous — matches {names!r}. Pass the UID instead.")
    return str(matches[0]["id"])


class _TrackedEntitiesEnvelope(BaseModel):
    """`{pager, instances: [...]}` envelope returned by /api/tracker/trackedEntities."""

    model_config = ConfigDict(extra="allow")

    instances: list[TrackerTrackedEntity] = []


class _EnrollmentsEnvelope(BaseModel):
    """`{pager, enrollments: [...]}` envelope."""

    model_config = ConfigDict(extra="allow")

    enrollments: list[TrackerEnrollment] = []


class _EventsEnvelope(BaseModel):
    """`{pager, events: [...]}` envelope."""

    model_config = ConfigDict(extra="allow")

    events: list[TrackerEvent] = []


class _RelationshipsEnvelope(BaseModel):
    """`{pager, instances: [...]}` envelope returned by /api/tracker/relationships."""

    model_config = ConfigDict(extra="allow")

    instances: list[TrackerRelationship] = []


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
) -> list[TrackerTrackedEntity]:
    """List tracked entities via GET /api/tracker/trackedEntities.

    At minimum, supply one of `program`, `tracked_entity_type`, or
    `tracked_entities` (comma-separated UIDs). `program` must point at a
    tracker program (programType=WITH_REGISTRATION).
    """
    params: dict[str, Any] = {"ouMode": ou_mode, "pageSize": page_size}
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
        raw = await client.get_raw("/api/tracker/trackedEntities", params=params)
    return _TrackedEntitiesEnvelope.model_validate(raw).instances


async def get_tracked_entity(
    profile: Profile,
    uid: str,
    *,
    program: str | None = None,
    fields: str | None = None,
) -> TrackerTrackedEntity:
    """Fetch one tracked entity by UID via GET /api/tracker/trackedEntities/{uid}."""
    params: dict[str, Any] = {}
    if program is not None:
        params["program"] = program
    if fields is not None:
        params["fields"] = fields
    async with open_client(profile) as client:
        raw = await client.get_raw(f"/api/tracker/trackedEntities/{uid}", params=params)
    return TrackerTrackedEntity.model_validate(raw)


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
) -> list[TrackerEnrollment]:
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
        raw = await client.get_raw("/api/tracker/enrollments", params=params)
    return _EnrollmentsEnvelope.model_validate(raw).enrollments


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
) -> list[TrackerEvent]:
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
        raw = await client.get_raw("/api/tracker/events", params=params)
    return _EventsEnvelope.model_validate(raw).events


async def list_relationships(
    profile: Profile,
    *,
    tracked_entity: str | None = None,
    enrollment: str | None = None,
    event: str | None = None,
    fields: str | None = None,
    page_size: int = 50,
) -> list[TrackerRelationship]:
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
        raw = await client.get_raw("/api/tracker/relationships", params=params)
    return _RelationshipsEnvelope.model_validate(raw).instances


async def push_tracker(
    profile: Profile,
    bundle: dict[str, Any],
    *,
    import_strategy: str | None = None,
    atomic_mode: str | None = None,
    dry_run: bool = False,
    async_mode: bool = False,
) -> WebMessageResponse:
    """Bulk import via POST /api/tracker with a bundle of tracker objects.

    The `bundle` envelope follows DHIS2's tracker payload shape:
      { "trackedEntities": [...], "enrollments": [...], "events": [...],
        "relationships": [...] }
    Any key may be omitted. `import_strategy` is one of `CREATE`, `UPDATE`,
    `CREATE_AND_UPDATE`, `DELETE`. `atomic_mode` is `ALL` or `OBJECT`.
    `dry_run=True` validates without writing. `async_mode=True` returns a job
    reference immediately (response.id = the job UID to poll).
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
        raw = await client.post_raw("/api/tracker", bundle, params=params)
    return WebMessageResponse.model_validate(raw)
