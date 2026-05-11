"""FastMCP tool registration for the `analytics` plugin."""

from __future__ import annotations

from typing import Any

from dhis2w_client.v42 import DataValueSet, Grid

from dhis2w_core.profile import resolve_profile
from dhis2w_core.v42.plugins.analytics import service


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
    ) -> Grid | DataValueSet:
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
    async def analytics_events_query(
        program: str,
        mode: str = "query",
        dimensions: list[str] | None = None,
        filters: list[str] | None = None,
        stage: str | None = None,
        output_type: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        skip_meta: bool = False,
        page: int | None = None,
        page_size: int | None = None,
        profile: str | None = None,
    ) -> Grid:
        """Run an event analytics query at /api/analytics/events/{mode}/{program}.

        `mode` is `query` (line-listed events) or `aggregate` (grouped counts).
        `stage` narrows to one ProgramStage UID. `output_type` picks the row
        shape: EVENT | ENROLLMENT | TRACKED_ENTITY_INSTANCE.
        """
        return await service.query_events(
            resolve_profile(profile),
            program=program,
            mode=mode,
            dimensions=dimensions,
            filters=filters,
            stage=stage,
            output_type=output_type,
            start_date=start_date,
            end_date=end_date,
            skip_meta=skip_meta,
            page=page,
            page_size=page_size,
        )

    @mcp.tool()
    async def analytics_enrollments_query(
        program: str,
        dimensions: list[str] | None = None,
        filters: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        skip_meta: bool = False,
        page: int | None = None,
        page_size: int | None = None,
        profile: str | None = None,
    ) -> Grid:
        """Run an enrollment analytics query at /api/analytics/enrollments/query/{program}."""
        return await service.query_enrollments(
            resolve_profile(profile),
            program=program,
            dimensions=dimensions,
            filters=filters,
            start_date=start_date,
            end_date=end_date,
            skip_meta=skip_meta,
            page=page,
            page_size=page_size,
        )

    @mcp.tool()
    async def analytics_outlier_detection(
        data_elements: list[str] | None = None,
        data_sets: list[str] | None = None,
        org_units: list[str] | None = None,
        periods: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        algorithm: str | None = None,
        threshold: float | None = None,
        max_results: int | None = None,
        order_by: str | None = None,
        sort_order: str | None = None,
        profile: str | None = None,
    ) -> Grid:
        """Run `/api/analytics/outlierDetection` — flag anomalous data values.

        `algorithm` is `Z_SCORE` (default), `MODIFIED_Z_SCORE`, or `MIN_MAX`. Supply
        either `data_elements` OR `data_sets` (the DS is expanded to its DEs);
        `org_units` + `periods` (or `start_date`/`end_date`) narrow the scope.

        Returns an `Grid` — the Grid envelope with `headers`
        and `rows`. Row columns typically include `dx`, `pe`, `ou`, `value`,
        `mean`, `stdDev`, `absDev`, `zScore` (check `headers` for the
        exact ordering).
        """
        return await service.query_outlier_detection(
            resolve_profile(profile),
            data_elements=data_elements,
            data_sets=data_sets,
            org_units=org_units,
            periods=periods,
            start_date=start_date,
            end_date=end_date,
            algorithm=algorithm,
            threshold=threshold,
            max_results=max_results,
            order_by=order_by,
            sort_order=sort_order,
        )

    @mcp.tool()
    async def analytics_tracked_entities_query(
        tracked_entity_type: str,
        dimensions: list[str] | None = None,
        filters: list[str] | None = None,
        program: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        ou_mode: str | None = None,
        display_property: str | None = None,
        skip_meta: bool = False,
        skip_data: bool = False,
        include_metadata_details: bool = False,
        page: int | None = None,
        page_size: int | None = None,
        asc: list[str] | None = None,
        desc: list[str] | None = None,
        profile: str | None = None,
    ) -> Grid:
        """Line-list tracked entities via `/api/analytics/trackedEntities/query/{trackedEntityType}`.

        `dimensions` + `filters` use the `dx:`/`pe:`/`ou:` compound syntax.
        `program` narrows to specific programs (repeatable). `ou_mode` is
        `SELECTED` / `CHILDREN` / `DESCENDANTS` / `ACCESSIBLE` / `ALL`.
        """
        return await service.query_tracked_entities(
            resolve_profile(profile),
            tracked_entity_type=tracked_entity_type,
            dimensions=dimensions,
            filters=filters,
            program=program,
            start_date=start_date,
            end_date=end_date,
            ou_mode=ou_mode,
            display_property=display_property,
            skip_meta=skip_meta,
            skip_data=skip_data,
            include_metadata_details=include_metadata_details,
            page=page,
            page_size=page_size,
            asc=asc,
            desc=desc,
        )
