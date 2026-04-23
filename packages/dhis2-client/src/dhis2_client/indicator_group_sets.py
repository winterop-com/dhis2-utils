"""IndicatorGroupSet authoring — `Dhis2Client.indicator_group_sets`.

An `IndicatorGroupSet` is the analytics dimension that collects
`IndicatorGroup`s — e.g. "Programme area" carries groups for each
disease programme; "Reporting quality" carries timeliness /
completeness groups. Mirrors `DataElementGroupSetsAccessor`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.schemas import IndicatorGroup, IndicatorGroupSet

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_INDICATOR_GROUP_SET_FIELDS: str = "id,name,shortName,code,description,compulsory,indicatorGroups[id,name,code]"


class IndicatorGroupSetsAccessor:
    """`Dhis2Client.indicator_group_sets` — CRUD + group-membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[IndicatorGroupSet]:
        """Return every IndicatorGroupSet with its groups inline."""
        raw = await self._client.get_raw(
            "/api/indicatorGroupSets",
            params={"fields": _INDICATOR_GROUP_SET_FIELDS, "paging": "false"},
        )
        rows = raw.get("indicatorGroupSets") or []
        return [IndicatorGroupSet.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> IndicatorGroupSet:
        """Fetch one group set by UID with its `indicatorGroups` populated."""
        raw = await self._client.get_raw(
            f"/api/indicatorGroupSets/{uid}",
            params={"fields": _INDICATOR_GROUP_SET_FIELDS},
        )
        return IndicatorGroupSet.model_validate(raw)

    async def list_groups(self, uid: str) -> list[IndicatorGroup]:
        """Return the groups in the set in definition order."""
        group_set = await self.get(uid)
        groups = group_set.indicatorGroups or []
        return [IndicatorGroup.model_validate(g) for g in groups if isinstance(g, dict)]

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        compulsory: bool = False,
    ) -> IndicatorGroupSet:
        """Create an empty group set; wire groups in via `add_groups`."""
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "compulsory": compulsory,
        }
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post_raw("/api/indicatorGroupSets", body=payload)
        created_uid = _uid_from_webmessage(envelope) or uid
        if not created_uid:
            raise RuntimeError("indicator-group-set create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group_set: IndicatorGroupSet) -> IndicatorGroupSet:
        """PUT an edited group set back. `group_set.id` must be set."""
        if not group_set.id:
            raise ValueError("update requires group_set.id to be set")
        body = group_set.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/indicatorGroupSets/{group_set.id}", body=body)
        return await self.get(group_set.id)

    async def add_groups(self, uid: str, *, group_uids: list[str]) -> IndicatorGroupSet:
        """Add `group_uids` to the set via the per-item POST shortcut."""
        for group_uid in group_uids:
            await self._client.post_raw(
                f"/api/indicatorGroupSets/{uid}/indicatorGroups/{group_uid}",
            )
        return await self.get(uid)

    async def remove_groups(self, uid: str, *, group_uids: list[str]) -> IndicatorGroupSet:
        """Drop `group_uids` from the set via the per-item DELETE shortcut."""
        for group_uid in group_uids:
            await self._client.delete_raw(
                f"/api/indicatorGroupSets/{uid}/indicatorGroups/{group_uid}",
            )
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete a group set — groups stay."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.delete_raw(f"/api/indicatorGroupSets/{uid}")


def _uid_from_webmessage(envelope: dict[str, Any]) -> str | None:
    """Pull the created UID out of DHIS2's `WebMessage` response envelope."""
    response = envelope.get("response")
    if isinstance(response, dict):
        uid = response.get("uid")
        if isinstance(uid, str):
            return uid
    return None


__all__ = [
    "IndicatorGroupSet",
    "IndicatorGroupSetsAccessor",
]
