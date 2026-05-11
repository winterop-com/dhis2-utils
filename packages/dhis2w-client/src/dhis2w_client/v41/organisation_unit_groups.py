"""OrganisationUnitGroup authoring — `Dhis2Client.organisation_unit_groups`.

DHIS2 groups organisation units by any orthogonal axis — ownership
(public/private), type (urban/rural), program participation — and
those groups are what analytics queries pivot on when you ask for a
breakdown by "facility type". This accessor wraps the generated CRUD
with the membership primitives integration code typically reaches for:

- `list_members` — page through the OUs in one group (the group-side
  inverse of `OrganisationUnit.organisationUnitGroups`).
- `add_members` / `remove_members` — set-diff style membership edits
  without hand-rolling the full group payload.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2w_client.generated.v41.schemas import OrganisationUnit, OrganisationUnitGroup

if TYPE_CHECKING:
    from dhis2w_client.v41.client import Dhis2Client
from dhis2w_client.v41.envelopes import WebMessageResponse

_OU_GROUP_FIELDS: str = "id,name,shortName,code,color,symbol,description,organisationUnits[id,name],groupSets[id,name]"
_MEMBER_FIELDS: str = "id,name,code,level,path"


class OrganisationUnitGroupsAccessor:
    """`Dhis2Client.organisation_unit_groups` — CRUD + membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[OrganisationUnitGroup]:
        """Return every OrganisationUnitGroup with its member refs inline."""
        return cast(
            list[OrganisationUnitGroup],
            await self._client.resources.organisation_unit_groups.list(
                fields=_OU_GROUP_FIELDS,
                paging=False,
            ),
        )

    async def get(self, uid: str) -> OrganisationUnitGroup:
        """Fetch one group by UID with `organisationUnits` + `groupSets` populated."""
        return await self._client.get(
            f"/api/organisationUnitGroups/{uid}", model=OrganisationUnitGroup, params={"fields": _OU_GROUP_FIELDS}
        )

    async def list_members(
        self,
        uid: str,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[OrganisationUnit]:
        """Page through OUs belonging to one group.

        Hits `/api/organisationUnits?filter=organisationUnitGroups.id:eq:<uid>`
        so pagination stays server-side — needed for province-level
        groups in large countries where a single group can carry
        thousands of facilities.
        """
        return cast(
            list[OrganisationUnit],
            await self._client.resources.organisation_units.list(
                fields=_MEMBER_FIELDS,
                filters=[f"organisationUnitGroups.id:eq:{uid}"],
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
        color: str | None = None,
        symbol: str | None = None,
    ) -> OrganisationUnitGroup:
        """Create an empty group; add members afterwards via `add_members`."""
        payload: dict[str, Any] = {"name": name, "shortName": short_name}
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        if color:
            payload["color"] = color
        if symbol:
            payload["symbol"] = symbol
        envelope = await self._client.post("/api/organisationUnitGroups", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("organisation-unit-group create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group: OrganisationUnitGroup) -> OrganisationUnitGroup:
        """PUT an edited group back. `group.id` must be set."""
        if not group.id:
            raise ValueError("update requires group.id to be set")
        body = group.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/organisationUnitGroups/{group.id}", body=body)
        return await self.get(group.id)

    async def add_members(self, uid: str, *, ou_uids: list[str]) -> OrganisationUnitGroup:
        """Add `ou_uids` to the group without clobbering existing members.

        DHIS2 exposes a direct `POST
        /api/organisationUnitGroups/{uid}/organisationUnits/{ou_uid}`
        shortcut for this — uses that per member so each add is one
        round-trip and the server never sees a payload with the full
        current membership.
        """
        for ou_uid in ou_uids:
            await self._client.resources.organisation_unit_groups.add_collection_item(uid, "organisationUnits", ou_uid)
        return await self.get(uid)

    async def remove_members(self, uid: str, *, ou_uids: list[str]) -> OrganisationUnitGroup:
        """Drop `ou_uids` from the group via the per-member DELETE shortcut."""
        for ou_uid in ou_uids:
            await self._client.resources.organisation_unit_groups.remove_collection_item(
                uid, "organisationUnits", ou_uid
            )
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete a group — members stay, only the grouping row is removed."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.organisation_unit_groups.delete(uid)


__all__ = [
    "OrganisationUnitGroup",
    "OrganisationUnitGroupsAccessor",
]
