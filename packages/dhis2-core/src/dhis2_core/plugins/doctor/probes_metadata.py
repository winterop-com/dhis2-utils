"""Instance-health probes — workspace-specific metadata sanity checks.

These answer "what's wrong with this instance's configuration" — the classes
of misconfiguration DHIS2 won't flag at startup but that cost operators real
time to debug:

- Data sets with no data elements (nothing to collect)
- Programs without stages (unusable)
- User groups with no members (likely stale)
- Category combos with no categories (broken metadata)
- Organisation units with no children, where children are expected
- ...

Each probe returns `offending_uids` so operators can jump straight to fixing
the flagged objects.
"""

from __future__ import annotations

from typing import Any

from dhis2_client import Dhis2Client

from dhis2_core.plugins.doctor._models import ProbeResult

# Cap how many UIDs we list per probe in the result. The number is in the
# message anyway; operators who want the full list should re-run with a
# targeted `dhis2 metadata list` query.
_MAX_OFFENDING_UIDS = 50


def _ids_of(items: list[dict[str, Any]]) -> list[str]:
    return [str(item["id"]) for item in items if "id" in item]


async def _list_all(client: Dhis2Client, resource: str, *, fields: str) -> list[dict[str, Any]]:
    """Fetch every row of a metadata resource (paging=false, single request)."""
    raw = await client.get_raw(f"/api/{resource}", params={"fields": fields, "paging": "false"})
    # DHIS2 returns the collection under the resource name key.
    items = raw.get(resource, [])
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def _summarise(name: str, offenders: list[str], message_when_none: str, message_when_some: str) -> ProbeResult:
    """Common result shape — `pass` on no offenders, `warn` with UIDs otherwise."""
    if not offenders:
        return ProbeResult(
            name=name,
            category="metadata",
            status="pass",
            message=message_when_none,
        )
    sample = offenders[:_MAX_OFFENDING_UIDS]
    return ProbeResult(
        name=name,
        category="metadata",
        status="warn",
        message=message_when_some.format(count=len(offenders)),
        offending_uids=sample,
        detail=(
            f"showing {len(sample)} of {len(offenders)} offending UIDs"
            if len(offenders) > _MAX_OFFENDING_UIDS
            else None
        ),
    )


async def probe_data_sets_without_data_elements(client: Dhis2Client) -> ProbeResult:
    """Flag data sets whose `dataSetElements` is empty — nothing to collect."""
    try:
        items = await _list_all(client, "dataSets", fields="id,name,dataSetElements~size")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="dataSets:dataElements",
            category="metadata",
            status="fail",
            message=f"/api/dataSets failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("dataSetElements", 0) or 0) == 0]
    return _summarise(
        "dataSets:dataElements",
        offenders,
        message_when_none=f"all {len(items)} data sets reference >=1 data element",
        message_when_some="{count} data set(s) have zero dataElements — nothing to collect",
    )


async def probe_data_sets_without_org_units(client: Dhis2Client) -> ProbeResult:
    """Flag data sets not assigned to any organisationUnit — users can't enter data.

    Overlap: DHIS2 has `datasets_not_assigned_to_org_units`. We keep ours for
    fast UID access without a prior `dataintegrity run`.
    """
    try:
        items = await _list_all(client, "dataSets", fields="id,name,organisationUnits~size")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="dataSets:orgUnits",
            category="metadata",
            status="fail",
            message=f"/api/dataSets failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("organisationUnits", 0) or 0) == 0]
    return _summarise(
        "dataSets:orgUnits",
        offenders,
        message_when_none=f"all {len(items)} data sets are assigned to >=1 organisationUnit",
        message_when_some="{count} data set(s) have zero organisationUnits — users can't enter data for them",
    )


async def probe_data_elements_without_data_sets(client: Dhis2Client) -> ProbeResult:
    """Flag data elements not attached to any data set (aggregate-domain only).

    Tracker-domain DEs are typically attached via programStageDataElements,
    not dataSetElements — only check `domainType=AGGREGATE`.

    Overlap: DHIS2 has `data_elements_without_datasets` (checks every DE, not
    just aggregate). We keep ours for the domain filter + instant UID access.
    """
    try:
        items = await _list_all(
            client,
            "dataElements",
            fields="id,name,domainType,dataSetElements~size",
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="dataElements",
            category="metadata",
            status="fail",
            message=f"/api/dataElements failed: {exc}",
        )
    aggregate = [item for item in items if item.get("domainType") == "AGGREGATE"]
    offenders = [str(item["id"]) for item in aggregate if int(item.get("dataSetElements", 0) or 0) == 0]
    return _summarise(
        "dataElements",
        offenders,
        message_when_none=(f"all {len(aggregate)} aggregate data elements are attached to >=1 dataSet"),
        message_when_some="{count} aggregate data element(s) aren't attached to any dataSet (orphan)",
    )


async def probe_programs_without_stages(client: Dhis2Client) -> ProbeResult:
    """Flag programs with no programStages — unusable."""
    try:
        items = await _list_all(client, "programs", fields="id,name,programStages~size")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="programs",
            category="metadata",
            status="fail",
            message=f"/api/programs failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("programStages", 0) or 0) == 0]
    return _summarise(
        "programs",
        offenders,
        message_when_none=f"all {len(items)} programs have >=1 stage",
        message_when_some="{count} program(s) have zero programStages — unusable",
    )


async def probe_user_groups_without_members(client: Dhis2Client) -> ProbeResult:
    """Flag user groups with no user members — likely stale metadata."""
    try:
        items = await _list_all(client, "userGroups", fields="id,name,users~size")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="userGroups",
            category="metadata",
            status="fail",
            message=f"/api/userGroups failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("users", 0) or 0) == 0]
    return _summarise(
        "userGroups",
        offenders,
        message_when_none=f"all {len(items)} user groups have >=1 member",
        message_when_some="{count} user group(s) have zero members — likely stale",
    )


async def probe_user_roles_without_members(client: Dhis2Client) -> ProbeResult:
    """Flag user roles not assigned to any user — dead roles.

    Overlap: DHIS2 has `user_roles_with_no_users`. We keep ours because our
    CLI surfaces the UID directly; the DHIS2 check needs `result --details`
    (plus a prior `run --details`) to get the same info.
    """
    try:
        items = await _list_all(client, "userRoles", fields="id,name,users~size")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="userRoles",
            category="metadata",
            status="fail",
            message=f"/api/userRoles failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("users", 0) or 0) == 0]
    return _summarise(
        "userRoles",
        offenders,
        message_when_none=f"all {len(items)} user roles have >=1 assigned user",
        message_when_some="{count} user role(s) have zero assigned users — dead roles",
    )


async def probe_category_combos_without_categories(client: Dhis2Client) -> ProbeResult:
    """Flag category combos with no categories — broken metadata (default CC may be empty too)."""
    try:
        items = await _list_all(
            client,
            "categoryCombos",
            fields="id,name,categories~size",
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="categoryCombos",
            category="metadata",
            status="fail",
            message=f"/api/categoryCombos failed: {exc}",
        )
    # DHIS2 always ships a "default" CC with no categories by design — filter by name.
    offenders = [
        str(item["id"])
        for item in items
        if int(item.get("categories", 0) or 0) == 0 and item.get("name", "").lower() != "default"
    ]
    return _summarise(
        "categoryCombos",
        offenders,
        message_when_none=f"all {len(items)} non-default category combos have >=1 category",
        message_when_some="{count} category combo(s) (excluding 'default') have zero categories",
    )


async def probe_org_unit_groups_without_members(client: Dhis2Client) -> ProbeResult:
    """Flag organisation-unit groups with no OU members — likely stale."""
    try:
        items = await _list_all(client, "organisationUnitGroups", fields="id,name,organisationUnits~size")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="organisationUnitGroups",
            category="metadata",
            status="fail",
            message=f"/api/organisationUnitGroups failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("organisationUnits", 0) or 0) == 0]
    return _summarise(
        "organisationUnitGroups",
        offenders,
        message_when_none=f"all {len(items)} org-unit groups have >=1 member",
        message_when_some="{count} org-unit group(s) have zero members — likely stale",
    )


async def probe_org_unit_group_sets_without_groups(client: Dhis2Client) -> ProbeResult:
    """Flag organisation-unit group sets with no groups — unusable in analytics."""
    try:
        items = await _list_all(
            client,
            "organisationUnitGroupSets",
            fields="id,name,organisationUnitGroups~size",
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="organisationUnitGroupSets",
            category="metadata",
            status="fail",
            message=f"/api/organisationUnitGroupSets failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("organisationUnitGroups", 0) or 0) == 0]
    return _summarise(
        "organisationUnitGroupSets",
        offenders,
        message_when_none=f"all {len(items)} org-unit group sets contain >=1 group",
        message_when_some="{count} org-unit group set(s) have zero groups — unusable in analytics",
    )


async def probe_dashboards_without_items(client: Dhis2Client) -> ProbeResult:
    """Flag dashboards with no items — empty landing pages.

    Overlap: DHIS2 has `dashboards_no_items`. We keep our probe because it
    returns `offending_uids` without needing a prior `dataintegrity run`.
    """
    try:
        items = await _list_all(client, "dashboards", fields="id,name,dashboardItems~size")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="dashboards",
            category="metadata",
            status="fail",
            message=f"/api/dashboards failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("dashboardItems", 0) or 0) == 0]
    return _summarise(
        "dashboards",
        offenders,
        message_when_none=f"all {len(items)} dashboards have >=1 item",
        message_when_some="{count} dashboard(s) have zero items — empty landing pages",
    )


async def probe_visualizations_without_dimensions(client: Dhis2Client) -> ProbeResult:
    """Flag visualizations with no data dimensions — empty charts."""
    try:
        items = await _list_all(
            client,
            "visualizations",
            fields="id,name,dataDimensionItems~size",
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="visualizations",
            category="metadata",
            status="fail",
            message=f"/api/visualizations failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if int(item.get("dataDimensionItems", 0) or 0) == 0]
    return _summarise(
        "visualizations",
        offenders,
        message_when_none=f"all {len(items)} visualizations have >=1 data dimension",
        message_when_some="{count} visualization(s) have zero dataDimensionItems — empty charts",
    )


async def probe_data_elements_missing_category_combo(client: Dhis2Client) -> ProbeResult:
    """Flag data elements missing a categoryCombo — broken metadata (every DE needs one)."""
    try:
        items = await _list_all(client, "dataElements", fields="id,name,categoryCombo")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="dataElements:categoryCombo",
            category="metadata",
            status="fail",
            message=f"/api/dataElements failed: {exc}",
        )
    offenders = [str(item["id"]) for item in items if not item.get("categoryCombo")]
    return _summarise(
        "dataElements:categoryCombo",
        offenders,
        message_when_none=f"all {len(items)} data elements reference a categoryCombo",
        message_when_some="{count} data element(s) have no categoryCombo — broken metadata",
    )


async def probe_indicators_with_empty_expressions(client: Dhis2Client) -> ProbeResult:
    """Flag indicators with an empty numerator OR denominator — unusable in analytics.

    Doesn't validate expression syntax — DHIS2 has `program_indicators_with_invalid_expressions`
    for that. This probe catches the simpler failure: a defined indicator where one of the
    two required expressions was never filled in.
    """
    try:
        items = await _list_all(client, "indicators", fields="id,name,numerator,denominator")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="indicators:expressions",
            category="metadata",
            status="fail",
            message=f"/api/indicators failed: {exc}",
        )
    # DHIS2 stores empty expressions as empty strings, not missing keys. Check both.
    offenders = [
        str(item["id"])
        for item in items
        if not str(item.get("numerator") or "").strip() or not str(item.get("denominator") or "").strip()
    ]
    return _summarise(
        "indicators:expressions",
        offenders,
        message_when_none=f"all {len(items)} indicators have a numerator + denominator",
        message_when_some="{count} indicator(s) have an empty numerator or denominator — unusable",
    )


async def probe_non_root_org_units_missing_parent(client: Dhis2Client) -> ProbeResult:
    """Flag non-root (level >= 2) org units missing a `parent` reference — broken hierarchy."""
    try:
        items = await _list_all(
            client,
            "organisationUnits",
            fields="id,name,level,parent",
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="organisationUnits:parent",
            category="metadata",
            status="fail",
            message=f"/api/organisationUnits failed: {exc}",
        )
    offenders: list[str] = []
    for item in items:
        # level == 1 is a valid root with no parent; higher levels must have one.
        try:
            level = int(item.get("level") or 0)
        except (TypeError, ValueError):
            level = 0
        parent = item.get("parent")
        if level >= 2 and not (isinstance(parent, dict) and parent.get("id")):
            offenders.append(str(item["id"]))
    return _summarise(
        "organisationUnits:parent",
        offenders,
        message_when_none=f"all {len(items)} org units have a valid parent (or are a level-1 root)",
        message_when_some="{count} non-root org unit(s) have no parent — broken hierarchy",
    )


METADATA_PROBES = (
    probe_data_sets_without_data_elements,
    probe_data_sets_without_org_units,
    probe_data_elements_without_data_sets,
    probe_data_elements_missing_category_combo,
    probe_programs_without_stages,
    probe_user_groups_without_members,
    probe_user_roles_without_members,
    probe_category_combos_without_categories,
    probe_org_unit_groups_without_members,
    probe_org_unit_group_sets_without_groups,
    probe_dashboards_without_items,
    probe_visualizations_without_dimensions,
    probe_indicators_with_empty_expressions,
    probe_non_root_org_units_missing_parent,
)
