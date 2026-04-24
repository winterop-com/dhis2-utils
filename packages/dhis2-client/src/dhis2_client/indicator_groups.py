"""IndicatorGroup authoring — `Dhis2Client.indicator_groups`.

`IndicatorGroup`s collect indicators by thematic axis (coverage,
quality, mortality, …) so dashboards and analytics can address a
coherent subset in one ref. Mirrors `DataElementGroupsAccessor`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.schemas import Indicator, IndicatorGroup

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client
from dhis2_client.envelopes import WebMessageResponse

_INDICATOR_GROUP_FIELDS: str = "id,name,shortName,code,description,indicators[id,name,code],groupSets[id,name]"
_MEMBER_FIELDS: str = "id,name,code,indicatorType[id,name]"


class IndicatorGroupsAccessor:
    """`Dhis2Client.indicator_groups` — CRUD + membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[IndicatorGroup]:
        """Return every IndicatorGroup."""
        raw = await self._client.get_raw(
            "/api/indicatorGroups",
            params={"fields": _INDICATOR_GROUP_FIELDS, "paging": "false"},
        )
        rows = raw.get("indicatorGroups") or []
        return [IndicatorGroup.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> IndicatorGroup:
        """Fetch one group by UID with `indicators` + `groupSets` populated."""
        return await self._client.get(
            f"/api/indicatorGroups/{uid}", model=IndicatorGroup, params={"fields": _INDICATOR_GROUP_FIELDS}
        )

    async def list_members(
        self,
        uid: str,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[Indicator]:
        """Page through Indicators belonging to one group."""
        raw = await self._client.get_raw(
            "/api/indicators",
            params={
                "filter": f"indicatorGroups.id:eq:{uid}",
                "fields": _MEMBER_FIELDS,
                "page": str(page),
                "pageSize": str(page_size),
                "order": "name:asc",
            },
        )
        rows = raw.get("indicators") or []
        return [Indicator.model_validate(row) for row in rows if isinstance(row, dict)]

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> IndicatorGroup:
        """Create an empty group; add members afterwards via `add_members`."""
        payload: dict[str, Any] = {"name": name, "shortName": short_name}
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post("/api/indicatorGroups", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("indicator-group create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group: IndicatorGroup) -> IndicatorGroup:
        """PUT an edited group back. `group.id` must be set."""
        if not group.id:
            raise ValueError("update requires group.id to be set")
        body = group.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/indicatorGroups/{group.id}", body=body)
        return await self.get(group.id)

    async def add_members(self, uid: str, *, indicator_uids: list[str]) -> IndicatorGroup:
        """Add Indicators to the group via the generated per-item POST shortcut."""
        for ind_uid in indicator_uids:
            await self._client.resources.indicator_groups.add_collection_item(uid, "indicators", ind_uid)
        return await self.get(uid)

    async def remove_members(self, uid: str, *, indicator_uids: list[str]) -> IndicatorGroup:
        """Drop Indicators from the group via the generated per-item DELETE shortcut."""
        for ind_uid in indicator_uids:
            await self._client.resources.indicator_groups.remove_collection_item(uid, "indicators", ind_uid)
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete the grouping row — member indicators stay."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.indicator_groups.delete(uid)


__all__ = [
    "IndicatorGroup",
    "IndicatorGroupsAccessor",
]
