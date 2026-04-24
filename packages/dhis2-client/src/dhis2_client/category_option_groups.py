"""CategoryOptionGroup authoring — `Dhis2Client.category_option_groups`.

`CategoryOptionGroup`s collect CategoryOptions thematically for
cross-disaggregation analysis (e.g. a `Maternal age bands` group
bundling several age CategoryOptions). Mirrors
`DataElementGroupsAccessor`: CRUD + per-item membership shortcuts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.schemas import CategoryOption, CategoryOptionGroup

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_COG_FIELDS: str = (
    "id,name,shortName,code,description,dataDimensionType,categoryOptions[id,name,code],groupSets[id,name]"
)
_MEMBER_FIELDS: str = "id,name,code,description"


class CategoryOptionGroupsAccessor:
    """`Dhis2Client.category_option_groups` — CRUD + membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[CategoryOptionGroup]:
        """Return every CategoryOptionGroup."""
        raw = await self._client.get_raw(
            "/api/categoryOptionGroups",
            params={"fields": _COG_FIELDS, "paging": "false"},
        )
        rows = raw.get("categoryOptionGroups") or []
        return [CategoryOptionGroup.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> CategoryOptionGroup:
        """Fetch one group by UID with `categoryOptions` + `groupSets` populated."""
        raw = await self._client.get_raw(
            f"/api/categoryOptionGroups/{uid}",
            params={"fields": _COG_FIELDS},
        )
        return CategoryOptionGroup.model_validate(raw)

    async def list_members(
        self,
        uid: str,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[CategoryOption]:
        """Page through CategoryOptions belonging to one group."""
        raw = await self._client.get_raw(
            "/api/categoryOptions",
            params={
                "filter": f"categoryOptionGroups.id:eq:{uid}",
                "fields": _MEMBER_FIELDS,
                "page": str(page),
                "pageSize": str(page_size),
                "order": "name:asc",
            },
        )
        rows = raw.get("categoryOptions") or []
        return [CategoryOption.model_validate(row) for row in rows if isinstance(row, dict)]

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        data_dimension_type: str = "DISAGGREGATION",
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> CategoryOptionGroup:
        """Create an empty group; add members afterwards via `add_members`.

        `data_dimension_type=DISAGGREGATION` (default) is the common case;
        `ATTRIBUTE` is the other value DHIS2 accepts — used when the group
        targets the attribute-combo grid (data source / funder / etc.)
        instead of the disaggregation grid (sex / age / etc.).
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "dataDimensionType": data_dimension_type,
        }
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post_raw("/api/categoryOptionGroups", body=payload)
        created_uid = _uid_from_webmessage(envelope) or uid
        if not created_uid:
            raise RuntimeError("category-option-group create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group: CategoryOptionGroup) -> CategoryOptionGroup:
        """PUT an edited group back. `group.id` must be set."""
        if not group.id:
            raise ValueError("update requires group.id to be set")
        body = group.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/categoryOptionGroups/{group.id}", body=body)
        return await self.get(group.id)

    async def add_members(self, uid: str, *, category_option_uids: list[str]) -> CategoryOptionGroup:
        """Add CategoryOptions to the group via the per-item POST shortcut."""
        for co_uid in category_option_uids:
            await self._client.resources.category_option_groups.add_collection_item(uid, "categoryOptions", co_uid)
        return await self.get(uid)

    async def remove_members(
        self,
        uid: str,
        *,
        category_option_uids: list[str],
    ) -> CategoryOptionGroup:
        """Drop CategoryOptions from the group via the per-item DELETE shortcut."""
        for co_uid in category_option_uids:
            await self._client.resources.category_option_groups.remove_collection_item(uid, "categoryOptions", co_uid)
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete the grouping row — member category options stay."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.category_option_groups.delete(uid)


def _uid_from_webmessage(envelope: dict[str, Any]) -> str | None:
    """Pull the created UID out of DHIS2's `WebMessage` response envelope."""
    response = envelope.get("response")
    if isinstance(response, dict):
        uid = response.get("uid")
        if isinstance(uid, str):
            return uid
    return None


__all__ = [
    "CategoryOptionGroup",
    "CategoryOptionGroupsAccessor",
]
