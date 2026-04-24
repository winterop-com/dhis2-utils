"""DataElementGroup authoring — `Dhis2Client.data_element_groups`.

DHIS2 `DataElementGroup`s collect data elements by thematic axis
(vaccines, antenatal indicators, HIV indicators, …) so dashboards,
pivot tables, and bulk metadata operations can target a coherent
subset in one ref. This accessor mirrors
`OrganisationUnitGroupsAccessor`: CRUD + per-item membership add/remove
via the DHIS2 collection-item shortcut routes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2_client.generated.v42.schemas import DataElement, DataElementGroup

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client
from dhis2_client.envelopes import WebMessageResponse

_DE_GROUP_FIELDS: str = "id,name,shortName,code,description,dataElements[id,name,code],groupSets[id,name]"
_MEMBER_FIELDS: str = "id,name,code,valueType,domainType"


class DataElementGroupsAccessor:
    """`Dhis2Client.data_element_groups` — CRUD + membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[DataElementGroup]:
        """Return every DataElementGroup with its member refs inline."""
        return cast(
            list[DataElementGroup],
            await self._client.resources.data_element_groups.list(
                fields=_DE_GROUP_FIELDS,
                paging=False,
            ),
        )

    async def get(self, uid: str) -> DataElementGroup:
        """Fetch one group by UID with `dataElements` + `groupSets` populated."""
        return await self._client.get(
            f"/api/dataElementGroups/{uid}", model=DataElementGroup, params={"fields": _DE_GROUP_FIELDS}
        )

    async def list_members(
        self,
        uid: str,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[DataElement]:
        """Page through DataElements belonging to one group."""
        return cast(
            list[DataElement],
            await self._client.resources.data_elements.list(
                fields=_MEMBER_FIELDS,
                filters=[f"dataElementGroups.id:eq:{uid}"],
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
    ) -> DataElementGroup:
        """Create an empty group; add members afterwards via `add_members`."""
        payload: dict[str, Any] = {"name": name, "shortName": short_name}
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post("/api/dataElementGroups", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("data-element-group create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group: DataElementGroup) -> DataElementGroup:
        """PUT an edited group back. `group.id` must be set."""
        if not group.id:
            raise ValueError("update requires group.id to be set")
        body = group.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/dataElementGroups/{group.id}", body=body)
        return await self.get(group.id)

    async def add_members(self, uid: str, *, data_element_uids: list[str]) -> DataElementGroup:
        """Add DataElements to the group via the per-item POST shortcut."""
        for de_uid in data_element_uids:
            await self._client.resources.data_element_groups.add_collection_item(uid, "dataElements", de_uid)
        return await self.get(uid)

    async def remove_members(self, uid: str, *, data_element_uids: list[str]) -> DataElementGroup:
        """Drop DataElements from the group via the per-item DELETE shortcut."""
        for de_uid in data_element_uids:
            await self._client.resources.data_element_groups.remove_collection_item(uid, "dataElements", de_uid)
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete the grouping row — member DEs stay."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.data_element_groups.delete(uid)


__all__ = [
    "DataElementGroup",
    "DataElementGroupsAccessor",
]
