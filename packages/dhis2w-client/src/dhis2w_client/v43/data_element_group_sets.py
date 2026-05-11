"""DataElementGroupSet authoring — `Dhis2Client.data_element_group_sets`.

A `DataElementGroupSet` is the analytics dimension that collects
`DataElementGroup`s — e.g. "Vaccine stock" carries groups for each
antigen, "HIV" carries groups for testing / treatment / care
indicators. Mirrors the OU-group-set surface: CRUD + per-item
`add_groups` / `remove_groups` via the DHIS2 collection-item shortcut
routes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2w_client.generated.v43.schemas import DataElementGroup, DataElementGroupSet

if TYPE_CHECKING:
    from dhis2w_client.v43.client import Dhis2Client
from dhis2w_client.v43.envelopes import WebMessageResponse

_DE_GROUP_SET_FIELDS: str = (
    "id,name,shortName,code,description,compulsory,dataDimension,dataElementGroups[id,name,code]"
)


class DataElementGroupSetsAccessor:
    """`Dhis2Client.data_element_group_sets` — CRUD + group-membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[DataElementGroupSet]:
        """Return every DataElementGroupSet with its groups inline."""
        return cast(
            list[DataElementGroupSet],
            await self._client.resources.data_element_group_sets.list(
                fields=_DE_GROUP_SET_FIELDS,
                paging=False,
            ),
        )

    async def get(self, uid: str) -> DataElementGroupSet:
        """Fetch one group set by UID with its `dataElementGroups` populated."""
        return await self._client.get(
            f"/api/dataElementGroupSets/{uid}", model=DataElementGroupSet, params={"fields": _DE_GROUP_SET_FIELDS}
        )

    async def list_groups(self, uid: str) -> list[DataElementGroup]:
        """Return the groups in the set in definition order."""
        group_set = await self.get(uid)
        groups = group_set.dataElementGroups or []
        return [DataElementGroup.model_validate(g) for g in groups if isinstance(g, dict)]

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        compulsory: bool = False,
        data_dimension: bool = True,
    ) -> DataElementGroupSet:
        """Create an empty group set; wire groups into it via `add_groups`.

        `data_dimension=True` (default) exposes the set as an analytics
        axis (pivot tables, visualisations). `compulsory=True` requires
        every member DE to land in exactly one group of the set.
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "compulsory": compulsory,
            "dataDimension": data_dimension,
        }
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post("/api/dataElementGroupSets", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("data-element-group-set create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group_set: DataElementGroupSet) -> DataElementGroupSet:
        """PUT an edited group set back. `group_set.id` must be set."""
        if not group_set.id:
            raise ValueError("update requires group_set.id to be set")
        body = group_set.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/dataElementGroupSets/{group_set.id}", body=body)
        return await self.get(group_set.id)

    async def add_groups(self, uid: str, *, group_uids: list[str]) -> DataElementGroupSet:
        """Add `group_uids` to the set via the per-item POST shortcut."""
        for group_uid in group_uids:
            await self._client.resources.data_element_group_sets.add_collection_item(
                uid, "dataElementGroups", group_uid
            )
        return await self.get(uid)

    async def remove_groups(self, uid: str, *, group_uids: list[str]) -> DataElementGroupSet:
        """Drop `group_uids` from the set via the per-item DELETE shortcut."""
        for group_uid in group_uids:
            await self._client.resources.data_element_group_sets.remove_collection_item(
                uid, "dataElementGroups", group_uid
            )
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete a group set — groups stay, only the dimension row is removed."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.data_element_group_sets.delete(uid)


__all__ = [
    "DataElementGroupSet",
    "DataElementGroupSetsAccessor",
]
