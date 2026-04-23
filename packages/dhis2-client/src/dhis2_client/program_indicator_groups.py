"""ProgramIndicatorGroup authoring — `Dhis2Client.program_indicator_groups`.

`ProgramIndicatorGroup`s collect program indicators thematically
(e.g. "Immunisation coverage", "HIV care continuum"). Smaller
surface than the aggregate-indicator group-set triple — DHIS2 does
*not* expose a `ProgramIndicatorGroupSet` resource, so this module
only covers the group layer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.schemas import ProgramIndicator, ProgramIndicatorGroup

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_PIG_FIELDS: str = "id,name,shortName,code,description,programIndicators[id,name,code]"
_MEMBER_FIELDS: str = "id,name,code,program[id,name]"


class ProgramIndicatorGroupsAccessor:
    """`Dhis2Client.program_indicator_groups` — CRUD + membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[ProgramIndicatorGroup]:
        """Return every ProgramIndicatorGroup."""
        raw = await self._client.get_raw(
            "/api/programIndicatorGroups",
            params={"fields": _PIG_FIELDS, "paging": "false"},
        )
        rows = raw.get("programIndicatorGroups") or []
        return [ProgramIndicatorGroup.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> ProgramIndicatorGroup:
        """Fetch one group by UID with its member refs populated."""
        raw = await self._client.get_raw(
            f"/api/programIndicatorGroups/{uid}",
            params={"fields": _PIG_FIELDS},
        )
        return ProgramIndicatorGroup.model_validate(raw)

    async def list_members(
        self,
        uid: str,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[ProgramIndicator]:
        """Page through ProgramIndicators inside one group."""
        raw = await self._client.get_raw(
            "/api/programIndicators",
            params={
                "filter": f"programIndicatorGroups.id:eq:{uid}",
                "fields": _MEMBER_FIELDS,
                "page": str(page),
                "pageSize": str(page_size),
                "order": "name:asc",
            },
        )
        rows = raw.get("programIndicators") or []
        return [ProgramIndicator.model_validate(row) for row in rows if isinstance(row, dict)]

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> ProgramIndicatorGroup:
        """Create an empty group; add members afterwards via `add_members`."""
        payload: dict[str, Any] = {"name": name, "shortName": short_name}
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post_raw("/api/programIndicatorGroups", body=payload)
        created_uid = _uid_from_webmessage(envelope) or uid
        if not created_uid:
            raise RuntimeError("program-indicator-group create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group: ProgramIndicatorGroup) -> ProgramIndicatorGroup:
        """PUT an edited group back. `group.id` must be set."""
        if not group.id:
            raise ValueError("update requires group.id to be set")
        body = group.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/programIndicatorGroups/{group.id}", body=body)
        return await self.get(group.id)

    async def add_members(self, uid: str, *, program_indicator_uids: list[str]) -> ProgramIndicatorGroup:
        """Add ProgramIndicators to the group via the per-item POST shortcut."""
        for pi_uid in program_indicator_uids:
            await self._client.post_raw(
                f"/api/programIndicatorGroups/{uid}/programIndicators/{pi_uid}",
            )
        return await self.get(uid)

    async def remove_members(self, uid: str, *, program_indicator_uids: list[str]) -> ProgramIndicatorGroup:
        """Drop ProgramIndicators from the group via the per-item DELETE shortcut."""
        for pi_uid in program_indicator_uids:
            await self._client.delete_raw(
                f"/api/programIndicatorGroups/{uid}/programIndicators/{pi_uid}",
            )
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete the grouping row — member program indicators stay."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.delete_raw(f"/api/programIndicatorGroups/{uid}")


def _uid_from_webmessage(envelope: dict[str, Any]) -> str | None:
    """Pull the created UID out of DHIS2's `WebMessage` response envelope."""
    response = envelope.get("response")
    if isinstance(response, dict):
        uid = response.get("uid")
        if isinstance(uid, str):
            return uid
    return None


__all__ = [
    "ProgramIndicatorGroup",
    "ProgramIndicatorGroupsAccessor",
]
