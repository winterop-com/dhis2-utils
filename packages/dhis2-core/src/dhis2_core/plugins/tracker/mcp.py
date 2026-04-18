"""FastMCP tools for the tracker domain — registered under `data_tracker_*`."""

from __future__ import annotations

from typing import Any

from dhis2_core.plugins.tracker import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register tracker tools (entity/enrollment/event/relationship + bulk push)."""

    @mcp.tool()
    async def data_tracker_entity_list(
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
        profile: str | None = None,
    ) -> dict[str, Any]:
        """List DHIS2 tracked entities.

        Requires one of `program` (tracker program UID), `tracked_entity_type`,
        or `tracked_entities` (comma-separated UIDs). `ou_mode` options are
        SELECTED, CHILDREN, DESCENDANTS, ACCESSIBLE, CAPTURE, ALL. `filter`
        follows DHIS2's `uid:operator:value` syntax. `profile` selects a named profile.
        """
        return await service.list_tracked_entities(
            resolve_profile(profile),
            program=program,
            tracked_entity_type=tracked_entity_type,
            tracked_entities=tracked_entities,
            org_unit=org_unit,
            ou_mode=ou_mode,
            fields=fields,
            filter=filter,
            page_size=page_size,
            page=page,
            updated_after=updated_after,
        )

    @mcp.tool()
    async def data_tracker_entity_get(
        uid: str,
        program: str | None = None,
        fields: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one DHIS2 tracked entity by UID."""
        return await service.get_tracked_entity(resolve_profile(profile), uid, program=program, fields=fields)

    @mcp.tool()
    async def data_tracker_enrollment_list(
        program: str | None = None,
        org_unit: str | None = None,
        ou_mode: str = "DESCENDANTS",
        tracked_entity: str | None = None,
        status: str | None = None,
        fields: str | None = None,
        page_size: int = 50,
        page: int | None = None,
        updated_after: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """List DHIS2 tracker enrollments.

        `status` filter values: ACTIVE, COMPLETED, CANCELLED. Tracker
        programs only (event programs have no enrollments).
        """
        return await service.list_enrollments(
            resolve_profile(profile),
            program=program,
            org_unit=org_unit,
            ou_mode=ou_mode,
            tracked_entity=tracked_entity,
            status=status,
            fields=fields,
            page_size=page_size,
            page=page,
            updated_after=updated_after,
        )

    @mcp.tool()
    async def data_tracker_event_list(
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
        profile: str | None = None,
    ) -> dict[str, Any]:
        """List DHIS2 tracker events.

        Works for both event programs (no registration) and tracker programs.
        `status` values: ACTIVE, COMPLETED, VISITED, SCHEDULE, OVERDUE, SKIPPED.
        Date filters are ISO YYYY-MM-DD.
        """
        return await service.list_events(
            resolve_profile(profile),
            program=program,
            program_stage=program_stage,
            org_unit=org_unit,
            ou_mode=ou_mode,
            tracked_entity=tracked_entity,
            enrollment=enrollment,
            status=status,
            occurred_after=occurred_after,
            occurred_before=occurred_before,
            fields=fields,
            page_size=page_size,
            page=page,
        )

    @mcp.tool()
    async def data_tracker_relationship_list(
        tracked_entity: str | None = None,
        enrollment: str | None = None,
        event: str | None = None,
        fields: str | None = None,
        page_size: int = 50,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """List DHIS2 relationships (one of tracked_entity/enrollment/event required)."""
        return await service.list_relationships(
            resolve_profile(profile),
            tracked_entity=tracked_entity,
            enrollment=enrollment,
            event=event,
            fields=fields,
            page_size=page_size,
        )

    @mcp.tool()
    async def data_tracker_push(
        bundle: dict[str, Any],
        import_strategy: str | None = None,
        atomic_mode: str | None = None,
        dry_run: bool = False,
        async_mode: bool = False,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Bulk import a tracker bundle via POST /api/tracker.

        The `bundle` envelope shape:
          {"trackedEntities": [...], "enrollments": [...], "events": [...], "relationships": [...]}
        Any key may be omitted. `import_strategy` options: CREATE, UPDATE,
        CREATE_AND_UPDATE, DELETE. `atomic_mode` options: ALL, OBJECT.
        `dry_run=True` validates without writing. `async_mode=True` returns a
        job reference immediately.
        """
        return await service.push_tracker(
            resolve_profile(profile),
            bundle,
            import_strategy=import_strategy,
            atomic_mode=atomic_mode,
            dry_run=dry_run,
            async_mode=async_mode,
        )
