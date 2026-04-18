"""Service layer for the `analytics` plugin — DHIS2 /api/analytics."""

from __future__ import annotations

from typing import Any

from dhis2_client import WebMessageResponse

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
) -> dict[str, Any]:
    """Run an analytics query. `shape` picks `table` (default), `raw`, or `dvs`.

    `dimensions` is a list of `dx:UID[;UID...]`, `pe:PERIOD[;PERIOD...]`,
    `ou:UID[;UID...]`, etc. `filters` follows the same syntax.
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
        return await client.get_raw(path, params=params)


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
