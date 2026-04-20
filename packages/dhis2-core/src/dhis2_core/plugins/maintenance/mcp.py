"""FastMCP tool registration for the `maintenance` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_client import (
    DataIntegrityCheck,
    DataIntegrityReport,
    Notification,
    WebMessageResponse,
)

from dhis2_core.plugins.maintenance import service
from dhis2_core.plugins.maintenance.service import SoftDeleteTarget
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register maintenance tools on the MCP server."""

    @mcp.tool()
    async def maintenance_task_types(profile: str | None = None) -> list[str]:
        """List every background-job type DHIS2 tracks under /api/system/tasks.

        Use one of these values as the `task_type` argument to the other task
        tools. Common ones: `ANALYTICS_TABLE`, `DATA_INTEGRITY`,
        `DATA_INTEGRITY_DETAILS`, `HOUSEKEEPING`, `METADATA_IMPORT`.
        """
        return await service.list_task_types(resolve_profile(profile))

    @mcp.tool()
    async def maintenance_task_list(task_type: str, profile: str | None = None) -> list[str]:
        """List every task UID recorded for a given job type (most-recent first)."""
        return await service.list_task_ids(resolve_profile(profile), task_type)

    @mcp.tool()
    async def maintenance_task_status(task_type: str, task_uid: str, profile: str | None = None) -> list[Notification]:
        """Return every notification emitted by a task, oldest first.

        A notification with `completed=true` marks the terminal state; the
        preceding rows track progress. Level is one of `INFO`, `WARN`, `ERROR`.
        """
        return await service.get_task_notifications(resolve_profile(profile), task_type, task_uid)

    @mcp.tool()
    async def maintenance_cache_clear(profile: str | None = None) -> dict[str, str]:
        """POST /api/maintenance/cache — clear every server-side cache."""
        await service.clear_cache(resolve_profile(profile))
        return {"status": "caches cleared"}

    @mcp.tool()
    async def maintenance_cleanup_soft_deleted(target: str, profile: str | None = None) -> dict[str, str]:
        """Hard-remove soft-deleted rows of the given kind.

        `target` is one of: `data-values`, `events`, `enrollments`,
        `tracked-entities`. DHIS2 keeps rows marked `deleted=true` for audit;
        this endpoint purges them, unblocking parent-metadata deletion
        (see BUGS.md #2).
        """
        await service.remove_soft_deleted(resolve_profile(profile), SoftDeleteTarget(target))
        return {"status": f"soft-deleted {target} removed"}

    @mcp.tool()
    async def maintenance_dataintegrity_checks(profile: str | None = None) -> list[DataIntegrityCheck]:
        """List every built-in data-integrity check definition."""
        return await service.list_dataintegrity_checks(resolve_profile(profile))

    @mcp.tool()
    async def maintenance_dataintegrity_run(
        checks: list[str] | None = None,
        details: bool = False,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Kick off a data-integrity run; returns the task envelope.

        `checks` is a list of check names (from `maintenance_dataintegrity_checks`);
        omit to run every check. `details=True` populates `issues[]`;
        `details=False` (default) only records `count`. Poll the task UID
        returned in `response.id` with `maintenance_task_status`.
        """
        return await service.run_dataintegrity(resolve_profile(profile), checks=checks, details=details)

    @mcp.tool()
    async def maintenance_dataintegrity_result(
        checks: list[str] | None = None,
        details: bool = False,
        profile: str | None = None,
    ) -> DataIntegrityReport:
        """Read the stored result of a completed data-integrity run (summary or details mode)."""
        if details:
            return await service.get_dataintegrity_details(resolve_profile(profile), checks=checks)
        return await service.get_dataintegrity_summary(resolve_profile(profile), checks=checks)

    @mcp.tool()
    async def maintenance_refresh_analytics(
        skip_resource_tables: bool = False,
        last_years: int | None = None,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Regenerate the analytics star schema (POST /api/resourceTables/analytics, job=ANALYTICS_TABLE).

        Primary post-ingest refresh workflow. Returns the typed task-ref
        envelope — pass to `maintenance_task_status` / a watch loop to
        track progress.
        """
        return await service.refresh_analytics(
            resolve_profile(profile),
            skip_resource_tables=skip_resource_tables,
            last_years=last_years,
        )

    @mcp.tool()
    async def maintenance_refresh_resource_tables(
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Regenerate resource tables only (POST /api/resourceTables, job=RESOURCE_TABLE).

        Rebuilds supporting OU / category hierarchy tables without touching
        the analytics star schema.
        """
        return await service.refresh_resource_tables(resolve_profile(profile))

    @mcp.tool()
    async def maintenance_refresh_monitoring(
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Regenerate monitoring tables (POST /api/resourceTables/monitoring, job=MONITORING).

        Rebuilds the tables backing data-quality / validation-rule monitoring.
        """
        return await service.refresh_monitoring(resolve_profile(profile))
