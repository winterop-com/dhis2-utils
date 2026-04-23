"""CategoryOptionGroupSet authoring — `Dhis2Client.category_option_group_sets`.

A `CategoryOptionGroupSet` is the analytics dimension that collects
`CategoryOptionGroup`s — e.g. "Programme funder" carries groups for
each disaggregated donor. Mirrors `DataElementGroupSetsAccessor`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.schemas import CategoryOptionGroup, CategoryOptionGroupSet

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_COGS_FIELDS: str = (
    "id,name,shortName,code,description,dataDimension,dataDimensionType,categoryOptionGroups[id,name,code]"
)


class CategoryOptionGroupSetsAccessor:
    """`Dhis2Client.category_option_group_sets` — CRUD + group-membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[CategoryOptionGroupSet]:
        """Return every CategoryOptionGroupSet."""
        raw = await self._client.get_raw(
            "/api/categoryOptionGroupSets",
            params={"fields": _COGS_FIELDS, "paging": "false"},
        )
        rows = raw.get("categoryOptionGroupSets") or []
        return [CategoryOptionGroupSet.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> CategoryOptionGroupSet:
        """Fetch one group set by UID with its groups inline."""
        raw = await self._client.get_raw(
            f"/api/categoryOptionGroupSets/{uid}",
            params={"fields": _COGS_FIELDS},
        )
        return CategoryOptionGroupSet.model_validate(raw)

    async def list_groups(self, uid: str) -> list[CategoryOptionGroup]:
        """Return the groups in the set, in definition order."""
        group_set = await self.get(uid)
        groups = group_set.categoryOptionGroups or []
        return [CategoryOptionGroup.model_validate(g) for g in groups if isinstance(g, dict)]

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        data_dimension_type: str = "DISAGGREGATION",
        data_dimension: bool = True,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> CategoryOptionGroupSet:
        """Create an empty group set; add groups via `add_groups`.

        `data_dimension=True` (the default) exposes the set as an
        analytics axis (pivot tables, visualisations).
        `data_dimension_type="DISAGGREGATION"` targets the disaggregation
        grid; `"ATTRIBUTE"` targets the attribute-combo grid (data
        source / funder / etc.).
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "dataDimensionType": data_dimension_type,
            "dataDimension": data_dimension,
        }
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post_raw("/api/categoryOptionGroupSets", body=payload)
        created_uid = _uid_from_webmessage(envelope) or uid
        if not created_uid:
            raise RuntimeError("category-option-group-set create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group_set: CategoryOptionGroupSet) -> CategoryOptionGroupSet:
        """PUT an edited group set back. `group_set.id` must be set."""
        if not group_set.id:
            raise ValueError("update requires group_set.id to be set")
        body = group_set.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/categoryOptionGroupSets/{group_set.id}", body=body)
        return await self.get(group_set.id)

    async def add_groups(self, uid: str, *, group_uids: list[str]) -> CategoryOptionGroupSet:
        """Add `group_uids` to the set via the per-item POST shortcut."""
        for group_uid in group_uids:
            await self._client.post_raw(
                f"/api/categoryOptionGroupSets/{uid}/categoryOptionGroups/{group_uid}",
            )
        return await self.get(uid)

    async def remove_groups(self, uid: str, *, group_uids: list[str]) -> CategoryOptionGroupSet:
        """Drop `group_uids` from the set via the per-item DELETE shortcut."""
        for group_uid in group_uids:
            await self._client.delete_raw(
                f"/api/categoryOptionGroupSets/{uid}/categoryOptionGroups/{group_uid}",
            )
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete a group set — groups stay."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.delete_raw(f"/api/categoryOptionGroupSets/{uid}")


def _uid_from_webmessage(envelope: dict[str, Any]) -> str | None:
    """Pull the created UID out of DHIS2's `WebMessage` response envelope."""
    response = envelope.get("response")
    if isinstance(response, dict):
        uid = response.get("uid")
        if isinstance(uid, str):
            return uid
    return None


__all__ = [
    "CategoryOptionGroupSet",
    "CategoryOptionGroupSetsAccessor",
]
