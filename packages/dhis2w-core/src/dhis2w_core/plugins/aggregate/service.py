"""Service layer for the `aggregate` plugin — DHIS2 aggregate data values.

Reads return a typed `DataValueSet` (with nested `DataValue` rows). Writes
return a typed `WebMessageResponse` envelope.
"""

from __future__ import annotations

from typing import Any

from dhis2w_client import DataValueSet, WebMessageResponse

from dhis2w_core.client_context import open_client
from dhis2w_core.profile import Profile


async def get_data_values(
    profile: Profile,
    *,
    data_set: str | None = None,
    period: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    org_unit: str | None = None,
    children: bool = False,
    data_element_group: str | None = None,
    limit: int | None = None,
) -> DataValueSet:
    """Fetch a data value set via GET /api/dataValueSets.

    DHIS2 requires a coherent combination of params — typically `dataSet`,
    `period` (or `startDate`+`endDate`), and `orgUnit`. `limit` truncates
    the `dataValues` list client-side after the response is parsed.
    """
    params: dict[str, Any] = {}
    if data_set is not None:
        params["dataSet"] = data_set
    if period is not None:
        params["period"] = period
    if start_date is not None:
        params["startDate"] = start_date
    if end_date is not None:
        params["endDate"] = end_date
    if org_unit is not None:
        params["orgUnit"] = org_unit
    if children:
        params["children"] = "true"
    if data_element_group is not None:
        params["dataElementGroup"] = data_element_group

    async with open_client(profile) as client:
        raw = await client.get_raw("/api/dataValueSets", params=params)
    envelope = DataValueSet.model_validate(raw)
    if limit is not None:
        envelope.dataValues = (envelope.dataValues or [])[:limit]
    return envelope


async def push_data_values(
    profile: Profile,
    data_values: list[dict[str, Any]],
    *,
    data_set: str | None = None,
    period: str | None = None,
    org_unit: str | None = None,
    dry_run: bool = False,
    preheat_cache: bool = True,
    import_strategy: str | None = None,
) -> WebMessageResponse:
    """Bulk push data values via POST /api/dataValueSets.

    `import_strategy` can be CREATE, UPDATE, CREATE_AND_UPDATE, DELETE (DHIS2 defaults
    to CREATE_AND_UPDATE). `dry_run=True` validates without writing. Use
    `response.import_count()` to get the typed ImportCount counters.
    """
    body: dict[str, Any] = {"dataValues": data_values}
    if data_set is not None:
        body["dataSet"] = data_set
    if period is not None:
        body["period"] = period
    if org_unit is not None:
        body["orgUnit"] = org_unit

    params: dict[str, Any] = {}
    if dry_run:
        params["dryRun"] = "true"
    if not preheat_cache:
        params["preheatCache"] = "false"
    if import_strategy is not None:
        params["importStrategy"] = import_strategy

    async with open_client(profile) as client:
        return await client.post("/api/dataValueSets", body, params=params, model=WebMessageResponse)


async def set_data_value(
    profile: Profile,
    *,
    data_element: str,
    period: str,
    org_unit: str,
    value: str,
    category_option_combo: str | None = None,
    attribute_option_combo: str | None = None,
    comment: str | None = None,
) -> WebMessageResponse:
    """Set a single data value via POST /api/dataValues (params-based)."""
    params: dict[str, Any] = {
        "de": data_element,
        "pe": period,
        "ou": org_unit,
        "value": value,
    }
    if category_option_combo is not None:
        params["co"] = category_option_combo
    if attribute_option_combo is not None:
        params["cc"] = attribute_option_combo
    if comment is not None:
        params["comment"] = comment

    async with open_client(profile) as client:
        return await client.post("/api/dataValues", body=None, params=params, model=WebMessageResponse)


async def delete_data_value(
    profile: Profile,
    *,
    data_element: str,
    period: str,
    org_unit: str,
    category_option_combo: str | None = None,
    attribute_option_combo: str | None = None,
) -> WebMessageResponse:
    """Delete a single data value via DELETE /api/dataValues."""
    params: dict[str, Any] = {"de": data_element, "pe": period, "ou": org_unit}
    if category_option_combo is not None:
        params["co"] = category_option_combo
    if attribute_option_combo is not None:
        params["cc"] = attribute_option_combo

    async with open_client(profile) as client:
        return await client.delete("/api/dataValues", params=params, model=WebMessageResponse)
