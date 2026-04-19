"""Service layer for the `analytics` plugin — DHIS2 /api/analytics.

`query_analytics` returns a typed pydantic model keyed off `shape`:

  shape="table" -> AnalyticsResponse   # headers + rows + metaData
  shape="raw"   -> AnalyticsResponse   # same envelope, pre-aggregation rows
  shape="dvs"   -> DataValueSet        # DataValueSet shape for import round-tripping
"""

from __future__ import annotations

from typing import Any

from dhis2_client import AnalyticsResponse, DataValueSet, WebMessageResponse

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile

_SHAPE_TO_PATH: dict[str, str] = {
    # v42+ MVC mapping quirk: rawData/dataValueSet sub-resources require the
    # explicit .json suffix even with Accept: application/json. The parent
    # /api/analytics path honours content negotiation normally. See BUGS.md #1.
    "table": "/api/analytics",
    "raw": "/api/analytics/rawData.json",
    "dvs": "/api/analytics/dataValueSet.json",
}


def _build_params(
    *,
    dimensions: list[str],
    filters: list[str] | None,
    aggregation_type: str | None,
    measure_criteria: str | None,
    skip_meta: bool,
    skip_data: bool,
    output_id_scheme: str | None,
    include_num_den: bool | None,
    display_property: str | None,
    start_date: str | None,
    end_date: str | None,
    relative_period_date: str | None,
) -> dict[str, Any]:
    params: dict[str, Any] = {"dimension": dimensions}
    if filters:
        params["filter"] = filters
    for key, value in (
        ("aggregationType", aggregation_type),
        ("measureCriteria", measure_criteria),
        ("outputIdScheme", output_id_scheme),
        ("displayProperty", display_property),
        ("startDate", start_date),
        ("endDate", end_date),
        ("relativePeriodDate", relative_period_date),
    ):
        if value is not None:
            params[key] = value
    if skip_meta:
        params["skipMeta"] = "true"
    if skip_data:
        params["skipData"] = "true"
    if include_num_den is not None:
        params["includeNumDen"] = "true" if include_num_den else "false"
    return params


async def query_analytics(
    profile: Profile,
    *,
    shape: str = "table",
    dimensions: list[str],
    filters: list[str] | None = None,
    aggregation_type: str | None = None,
    measure_criteria: str | None = None,
    skip_meta: bool = False,
    skip_data: bool = False,
    output_id_scheme: str | None = None,
    include_num_den: bool | None = None,
    display_property: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    relative_period_date: str | None = None,
) -> AnalyticsResponse | DataValueSet:
    """Run an analytics query. `shape` picks `table` (default), `raw`, or `dvs`.

    `dimensions` is a list of `dx:UID[;UID...]`, `pe:PERIOD[;PERIOD...]`,
    `ou:UID[;UID...]`, etc. `filters` follows the same syntax.

    Return type varies with `shape`:
      - `table` / `raw` → `AnalyticsResponse` (headers/rows/metaData envelope)
      - `dvs`           → `DataValueSet` (round-trippable into /api/dataValueSets)
    """
    path = _SHAPE_TO_PATH.get(shape)
    if path is None:
        raise ValueError(f"unknown analytics shape {shape!r}; valid: {sorted(_SHAPE_TO_PATH)}")
    params = _build_params(
        dimensions=dimensions,
        filters=filters,
        aggregation_type=aggregation_type,
        measure_criteria=measure_criteria,
        skip_meta=skip_meta,
        skip_data=skip_data,
        output_id_scheme=output_id_scheme,
        include_num_den=include_num_den,
        display_property=display_property,
        start_date=start_date,
        end_date=end_date,
        relative_period_date=relative_period_date,
    )
    async with open_client(profile) as client:
        raw = await client.get_raw(path, params=params)
    if shape == "dvs":
        return DataValueSet.model_validate(raw)
    return AnalyticsResponse.model_validate(raw)


async def query_events(
    profile: Profile,
    *,
    program: str,
    mode: str = "query",
    stage: str | None = None,
    dimensions: list[str] | None = None,
    filters: list[str] | None = None,
    output_type: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    skip_meta: bool = False,
    page: int | None = None,
    page_size: int | None = None,
) -> AnalyticsResponse:
    """Run an event analytics query at `/api/analytics/events/{mode}/{program}`.

    `mode` is either `query` (line-listed events) or `aggregate` (aggregated
    counts bucketed by the supplied dimensions). `stage` narrows to one
    `ProgramStage` UID; `output_type` picks which row shape DHIS2 returns
    (`EVENT`, `ENROLLMENT`, `TRACKED_ENTITY_INSTANCE`).

    The response envelope is the same shape as `/api/analytics` — headers,
    rows, metaData — so callers can reuse the `AnalyticsResponse` helpers.
    """
    if mode not in {"query", "aggregate"}:
        raise ValueError(f"unknown event analytics mode {mode!r}; valid: ['aggregate', 'query']")
    params = _build_event_params(
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
    path = f"/api/analytics/events/{mode}/{program}"
    async with open_client(profile) as client:
        raw = await client.get_raw(path, params=params)
    return AnalyticsResponse.model_validate(raw)


async def query_enrollments(
    profile: Profile,
    *,
    program: str,
    dimensions: list[str] | None = None,
    filters: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    skip_meta: bool = False,
    page: int | None = None,
    page_size: int | None = None,
) -> AnalyticsResponse:
    """Run an enrollment analytics query at `/api/analytics/enrollments/query/{program}`.

    Line-lists enrollments in `program` over the supplied period/org-unit
    dimensions. No aggregated variant exists on this endpoint — DHIS2 only
    ships `/enrollments/query`. Response envelope matches `AnalyticsResponse`.
    """
    params = _build_event_params(
        dimensions=dimensions,
        filters=filters,
        stage=None,
        output_type=None,
        start_date=start_date,
        end_date=end_date,
        skip_meta=skip_meta,
        page=page,
        page_size=page_size,
    )
    path = f"/api/analytics/enrollments/query/{program}"
    async with open_client(profile) as client:
        raw = await client.get_raw(path, params=params)
    return AnalyticsResponse.model_validate(raw)


def _build_event_params(
    *,
    dimensions: list[str] | None,
    filters: list[str] | None,
    stage: str | None,
    output_type: str | None,
    start_date: str | None,
    end_date: str | None,
    skip_meta: bool,
    page: int | None,
    page_size: int | None,
) -> dict[str, Any]:
    """Build the query-string for event/enrollment analytics endpoints."""
    params: dict[str, Any] = {}
    if dimensions:
        params["dimension"] = dimensions
    if filters:
        params["filter"] = filters
    for key, value in (
        ("stage", stage),
        ("outputType", output_type),
        ("startDate", start_date),
        ("endDate", end_date),
    ):
        if value is not None:
            params[key] = value
    if skip_meta:
        params["skipMeta"] = "true"
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    return params


async def refresh_analytics(
    profile: Profile,
    *,
    skip_resource_tables: bool = False,
    last_years: int | None = None,
) -> WebMessageResponse:
    """Trigger analytics-table regeneration via POST /api/resourceTables/analytics.

    Returns a typed `JobConfigurationWebMessageResponse` envelope wrapped by
    `WebMessageResponse`. Use `.created_uid` for the task UID and poll
    `/api/system/tasks/ANALYTICS_TABLE/{taskId}` for status.
    """
    params: dict[str, Any] = {}
    if skip_resource_tables:
        params["skipResourceTables"] = "true"
    if last_years is not None:
        params["lastYears"] = last_years
    async with open_client(profile) as client:
        raw = await client.post_raw("/api/resourceTables/analytics", params=params)
    return WebMessageResponse.model_validate(raw)
