"""Service layer for the `analytics` plugin — DHIS2 /api/analytics.

`query_analytics` returns a typed pydantic model keyed off `shape`:

  shape="table" -> Grid   # headers + rows + metaData
  shape="raw"   -> Grid   # same envelope, pre-aggregation rows
  shape="dvs"   -> DataValueSet        # DataValueSet shape for import round-tripping
"""

from __future__ import annotations

from typing import Any

from dhis2w_client import DataValueSet, Grid

from dhis2w_core.client_context import open_client
from dhis2w_core.profile import Profile

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
) -> Grid | DataValueSet:
    """Run an analytics query. `shape` picks `table` (default), `raw`, or `dvs`.

    `dimensions` is a list of `dx:UID[;UID...]`, `pe:PERIOD[;PERIOD...]`,
    `ou:UID[;UID...]`, etc. `filters` follows the same syntax.

    Return type varies with `shape`:
      - `table` / `raw` → `Grid` (headers/rows/metaData envelope)
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
    return Grid.model_validate(raw)


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
) -> Grid:
    """Run an event analytics query at `/api/analytics/events/{mode}/{program}`.

    `mode` is either `query` (line-listed events) or `aggregate` (aggregated
    counts bucketed by the supplied dimensions). `stage` narrows to one
    `ProgramStage` UID; `output_type` picks which row shape DHIS2 returns
    (`EVENT`, `ENROLLMENT`, `TRACKED_ENTITY_INSTANCE`).

    The response envelope is the same shape as `/api/analytics` — headers,
    rows, metaData — so callers can reuse the `Grid` helpers.
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
    return Grid.model_validate(raw)


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
) -> Grid:
    """Run an enrollment analytics query at `/api/analytics/enrollments/query/{program}`.

    Line-lists enrollments in `program` over the supplied period/org-unit
    dimensions. No aggregated variant exists on this endpoint — DHIS2 only
    ships `/enrollments/query`. Response envelope matches `Grid`.
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
    return Grid.model_validate(raw)


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


async def query_outlier_detection(
    profile: Profile,
    *,
    data_elements: list[str] | None = None,
    data_sets: list[str] | None = None,
    org_units: list[str] | None = None,
    periods: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    data_start_date: str | None = None,
    data_end_date: str | None = None,
    algorithm: str | None = None,
    threshold: float | None = None,
    max_results: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    output_id_scheme: str | None = None,
) -> Grid:
    """Run an outlier-detection analysis via `GET /api/analytics/outlierDetection`.

    DHIS2 accepts dimensions via the named query params (not the `dx:`/`pe:`
    compound form used by `query_analytics`):
    `dx` (data elements), `ds` (data sets), `ou` (org units), `pe`
    (single period). `algorithm` is one of `Z_SCORE`, `MODIFIED_Z_SCORE`,
    `MIN_MAX`; `threshold` sets the standard-deviation cutoff (default 3.0
    server-side).

    Returns an `Grid` (the Grid envelope — headers + rows).
    Each row is ordered per the `headers` list; typical fields include
    `dx`, `pe`, `ou`, `value`, `mean`, `stdDev`, `absDev`, `zScore`. Note:
    DHIS2's OpenAPI schema documents a separate `OutlierDetectionResponse`
    type, but the wire format is actually `Grid` — see BUGS.md for the
    schema-vs-reality divergence.
    """
    params: dict[str, Any] = {}
    if data_elements:
        params["dx"] = data_elements
    if data_sets:
        params["ds"] = data_sets
    if org_units:
        params["ou"] = org_units
    for key, value in (
        ("pe", periods),
        ("startDate", start_date),
        ("endDate", end_date),
        ("dataStartDate", data_start_date),
        ("dataEndDate", data_end_date),
        ("algorithm", algorithm),
        ("threshold", threshold),
        ("maxResults", max_results),
        ("orderBy", order_by),
        ("sortOrder", sort_order),
        ("outputIdScheme", output_id_scheme),
    ):
        if value is not None:
            params[key] = value
    async with open_client(profile) as client:
        raw = await client.get_raw("/api/analytics/outlierDetection", params=params)
    return Grid.model_validate(raw)


async def query_tracked_entities(
    profile: Profile,
    *,
    tracked_entity_type: str,
    dimensions: list[str] | None = None,
    filters: list[str] | None = None,
    program: list[str] | None = None,
    enrollment_date: list[str] | None = None,
    event_date: list[str] | None = None,
    incident_date: list[str] | None = None,
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
) -> Grid:
    """Line-list tracked entities via `GET /api/analytics/trackedEntities/query/{trackedEntityType}`.

    Parallels `query_events` / `query_enrollments` shape but hangs off the
    TET. `dimensions` and `filters` follow the `dx:`/`pe:`/`ou:` compound
    syntax of the other analytics endpoints. Response envelope matches
    `Grid` (headers / rows / metaData). Useful for exporting a
    TET slice for external BI or building a registry view.
    """
    params: dict[str, Any] = {}
    if dimensions:
        params["dimension"] = dimensions
    if filters:
        params["filter"] = filters
    if program:
        params["program"] = program
    if enrollment_date:
        params["enrollmentDate"] = enrollment_date
    if event_date:
        params["eventDate"] = event_date
    if incident_date:
        params["incidentDate"] = incident_date
    if asc:
        params["asc"] = asc
    if desc:
        params["desc"] = desc
    for key, value in (
        ("startDate", start_date),
        ("endDate", end_date),
        ("ouMode", ou_mode),
        ("displayProperty", display_property),
        ("page", page),
        ("pageSize", page_size),
    ):
        if value is not None:
            params[key] = value
    if skip_meta:
        params["skipMeta"] = "true"
    if skip_data:
        params["skipData"] = "true"
    if include_metadata_details:
        params["includeMetadataDetails"] = "true"
    async with open_client(profile) as client:
        raw = await client.get_raw(
            f"/api/analytics/trackedEntities/query/{tracked_entity_type}",
            params=params,
        )
    return Grid.model_validate(raw)
