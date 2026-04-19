"""FastMCP tool registration for the `analytics` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_client import AnalyticsResponse, DataValueSet, WebMessageResponse

from dhis2_core.plugins.analytics import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register analytics tools on the MCP server."""

    @mcp.tool()
    async def analytics_query(
        dimensions: list[str],
        shape: str = "table",
        filters: list[str] | None = None,
        aggregation_type: str | None = None,
        output_id_scheme: str | None = None,
        include_num_den: bool | None = None,
        display_property: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        skip_meta: bool = False,
        profile: str | None = None,
    ) -> AnalyticsResponse | DataValueSet:
        """Run a DHIS2 analytics query.

        `dimensions` is a list like ['dx:fbfJHSPpUQD;cYeuwXTCPkU', 'pe:LAST_12_MONTHS', 'ou:ImspTQPwCqd'].
        `dx` = data elements / indicators, `pe` = periods, `ou` = org units.
        `filters` uses the same syntax.

        `shape` picks the response format:
          - `table` (default): aggregated rows, /api/analytics.
          - `raw`: pre-aggregation rows, /api/analytics/rawData.
          - `dvs`: DataValueSet envelope (round-trippable into dataValueSets import).

        `aggregation_type`: SUM, AVERAGE, COUNT, MIN, MAX, etc.
        `output_id_scheme`: UID (default), NAME, CODE, ID.
        `profile` selects a named profile.
        """
        return await service.query_analytics(
            resolve_profile(profile),
            shape=shape,
            dimensions=dimensions,
            filters=filters,
            aggregation_type=aggregation_type,
            output_id_scheme=output_id_scheme,
            include_num_den=include_num_den,
            display_property=display_property,
            start_date=start_date,
            end_date=end_date,
            skip_meta=skip_meta,
        )

    @mcp.tool()
    async def analytics_refresh(
        skip_resource_tables: bool = False,
        last_years: int | None = None,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Trigger analytics-table regeneration via POST /api/resourceTables/analytics.

        Returns the DHIS2 task reference. Poll
        `/api/system/tasks/ANALYTICS_TABLE/{taskId}` to track progress.
        """
        return await service.refresh_analytics(
            resolve_profile(profile),
            skip_resource_tables=skip_resource_tables,
            last_years=last_years,
        )
