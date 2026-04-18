"""FastMCP tool registration for the `analytics` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_core.plugins.analytics import service
from dhis2_core.profile import profile_from_env


def register(mcp: Any) -> None:
    """Register analytics tools on the MCP server."""

    @mcp.tool()
    async def query_analytics(
        dimensions: list[str],
        filters: list[str] | None = None,
        aggregation_type: str | None = None,
        output_id_scheme: str | None = None,
        include_num_den: bool | None = None,
        display_property: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        skip_meta: bool = False,
    ) -> dict[str, Any]:
        """Run a DHIS2 aggregated analytics query.

        `dimensions` is a list like ['dx:fbfJHSPpUQD;cYeuwXTCPkU', 'pe:LAST_12_MONTHS', 'ou:ImspTQPwCqd'].
        `dx` = data elements / indicators, `pe` = periods, `ou` = org units.
        `filters` uses the same syntax. `aggregation_type`: SUM, AVERAGE, COUNT, MIN,
        MAX, etc. `output_id_scheme`: UID (default), NAME, CODE, ID.
        Returns the standard analytics response with `headers`, `rows`, `metaData`.
        """
        return await service.query_analytics(
            profile_from_env(),
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
    async def query_analytics_raw(
        dimensions: list[str],
        filters: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        skip_meta: bool = False,
    ) -> dict[str, Any]:
        """Run a raw-data analytics query (/api/analytics/rawData).

        Unlike `query_analytics`, this variant returns the pre-aggregation rows
        suitable for client-side aggregation. Same dimension/filter syntax.
        """
        return await service.query_analytics_raw(
            profile_from_env(),
            dimensions=dimensions,
            filters=filters,
            start_date=start_date,
            end_date=end_date,
            skip_meta=skip_meta,
        )

    @mcp.tool()
    async def query_analytics_data_value_set(
        dimensions: list[str],
        filters: list[str] | None = None,
        output_id_scheme: str | None = None,
    ) -> dict[str, Any]:
        """Run analytics returning the DataValueSet shape (for downstream pipelines)."""
        return await service.query_analytics_data_value_set(
            profile_from_env(),
            dimensions=dimensions,
            filters=filters,
            output_id_scheme=output_id_scheme,
        )

    @mcp.tool()
    async def refresh_analytics(
        skip_resource_tables: bool = False,
        last_years: int | None = None,
    ) -> dict[str, Any]:
        """Trigger analytics-table regeneration via POST /api/resourceTables/analytics.

        Returns the DHIS2 task reference. Poll
        `/api/system/tasks/ANALYTICS_TABLE/{taskId}` to track progress.
        """
        return await service.refresh_analytics(
            profile_from_env(),
            skip_resource_tables=skip_resource_tables,
            last_years=last_years,
        )
