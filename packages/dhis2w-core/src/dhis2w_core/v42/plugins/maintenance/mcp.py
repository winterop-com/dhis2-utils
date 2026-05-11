"""FastMCP tool registration for the `maintenance` plugin."""

from __future__ import annotations

from typing import Any

from dhis2w_client.generated.v42.oas import ValidationResult
from dhis2w_client.v42 import (
    DataIntegrityCheck,
    DataIntegrityReport,
    ExpressionDescription,
    Notification,
    ValidationAnalysisResult,
    WebMessageResponse,
)

from dhis2w_core.profile import resolve_profile
from dhis2w_core.v42.plugins.maintenance import service
from dhis2w_core.v42.plugins.maintenance.service import SoftDeleteTarget


def register(mcp: Any) -> None:
    """Register maintenance tools on the MCP server."""

    @mcp.tool()
    async def maintenance_task_type_list(profile: str | None = None) -> list[str]:
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

    @mcp.tool()
    async def maintenance_validation_run(
        org_unit: str,
        start_date: str,
        end_date: str,
        validation_rule_group: str | None = None,
        max_results: int | None = None,
        notification: bool = False,
        persist: bool = False,
        profile: str | None = None,
    ) -> list[ValidationAnalysisResult]:
        """Run a validation-rule analysis synchronously + return violations.

        `org_unit` is the root of the sub-tree DHIS2 walks. `persist=True`
        writes violations into `/api/validationResults` so later list calls
        can walk them; `notification=True` fires configured templates.
        """
        return await service.run_validation_analysis(
            resolve_profile(profile),
            org_unit=org_unit,
            start_date=start_date,
            end_date=end_date,
            validation_rule_group=validation_rule_group,
            max_results=max_results,
            notification=notification,
            persist=persist,
        )

    @mcp.tool()
    async def maintenance_validation_result_list(
        org_unit: str | None = None,
        period: str | None = None,
        validation_rule: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        profile: str | None = None,
    ) -> list[ValidationResult]:
        """List persisted validation results, with optional filters."""
        return await service.list_validation_results(
            resolve_profile(profile),
            org_unit=org_unit,
            period=period,
            validation_rule=validation_rule,
            page=page,
            page_size=page_size,
        )

    @mcp.tool()
    async def maintenance_validation_validate_expression(
        expression: str,
        context: str = "generic",
        profile: str | None = None,
    ) -> ExpressionDescription:
        """Parse-check a DHIS2 expression + render a human description.

        `context` picks the parser: one of `generic` / `validation-rule` /
        `indicator` / `predictor` / `program-indicator`. Each has a
        different allowed-reference set (e.g. indicators allow
        `#{ou.de}` refs, predictors allow sample-function calls, etc.).
        """
        from dhis2w_client.v42 import ExpressionContext  # noqa: PLC0415

        if context not in ("generic", "validation-rule", "indicator", "predictor", "program-indicator"):
            raise ValueError(
                f"unknown expression context {context!r}; valid: "
                "generic, validation-rule, indicator, predictor, program-indicator",
            )
        typed_context: ExpressionContext = context  # type: ignore[assignment]
        return await service.describe_expression(
            resolve_profile(profile),
            expression,
            context=typed_context,
        )

    @mcp.tool()
    async def maintenance_predictors_run(
        start_date: str,
        end_date: str,
        predictor_uid: str | None = None,
        group_uid: str | None = None,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Run predictor expressions + emit data values.

        Pass `predictor_uid` to run one predictor, `group_uid` to run a
        PredictorGroup, or neither to run every predictor on the instance.
        """
        return await service.run_predictors(
            resolve_profile(profile),
            start_date=start_date,
            end_date=end_date,
            predictor_uid=predictor_uid,
            group_uid=group_uid,
        )
