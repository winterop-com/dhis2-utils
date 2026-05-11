"""ProgramIndicatorGroup authoring — `Dhis2Client.program_indicator_groups`.

`ProgramIndicatorGroup`s collect program indicators thematically
(e.g. "Immunisation coverage", "HIV care continuum"). Smaller
surface than the aggregate-indicator group-set triple — DHIS2 does
*not* expose a `ProgramIndicatorGroupSet` resource, so this module
only covers the group layer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2w_client.generated.v42.schemas import ProgramIndicator, ProgramIndicatorGroup

if TYPE_CHECKING:
    from dhis2w_client.v41.client import Dhis2Client
from dhis2w_client.v41.envelopes import WebMessageResponse

_PIG_FIELDS: str = "id,name,shortName,code,description,programIndicators[id,name,code]"
_MEMBER_FIELDS: str = "id,name,code,program[id,name]"


class ProgramIndicatorGroupsAccessor:
    """`Dhis2Client.program_indicator_groups` — CRUD + membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[ProgramIndicatorGroup]:
        """Return every ProgramIndicatorGroup."""
        return cast(
            list[ProgramIndicatorGroup],
            await self._client.resources.program_indicator_groups.list(
                fields=_PIG_FIELDS,
                paging=False,
            ),
        )

    async def get(self, uid: str) -> ProgramIndicatorGroup:
        """Fetch one group by UID with its member refs populated."""
        return await self._client.get(
            f"/api/programIndicatorGroups/{uid}", model=ProgramIndicatorGroup, params={"fields": _PIG_FIELDS}
        )

    async def list_members(
        self,
        uid: str,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[ProgramIndicator]:
        """Page through ProgramIndicators inside one group."""
        return cast(
            list[ProgramIndicator],
            await self._client.resources.program_indicators.list(
                fields=_MEMBER_FIELDS,
                filters=[f"programIndicatorGroups.id:eq:{uid}"],
                order=["name:asc"],
                page=page,
                page_size=page_size,
            ),
        )

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
        envelope = await self._client.post("/api/programIndicatorGroups", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
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
            await self._client.resources.program_indicator_groups.add_collection_item(uid, "programIndicators", pi_uid)
        return await self.get(uid)

    async def remove_members(self, uid: str, *, program_indicator_uids: list[str]) -> ProgramIndicatorGroup:
        """Drop ProgramIndicators from the group via the per-item DELETE shortcut."""
        for pi_uid in program_indicator_uids:
            await self._client.resources.program_indicator_groups.remove_collection_item(
                uid, "programIndicators", pi_uid
            )
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete the grouping row — member program indicators stay."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.program_indicator_groups.delete(uid)


__all__ = [
    "ProgramIndicatorGroup",
    "ProgramIndicatorGroupsAccessor",
]
