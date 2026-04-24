"""OrganisationUnitGroupSet authoring — `Dhis2Client.organisation_unit_group_sets`.

A DHIS2 `OrganisationUnitGroupSet` is the analytics *dimension* that
groups `OrganisationUnitGroup`s: "Facility Ownership" carries the
public/private/NGO groups, "Facility Type" carries urban/rural, etc.
Visualisations and pivot tables reference a group set by UID to get a
named axis off the OU hierarchy. This accessor wraps the generated
CRUD with the membership primitives authoring flows need:

- `list_groups` — enumerate groups inside one set.
- `add_groups` / `remove_groups` — set-diff membership edits via the
  per-item DELETE/POST shortcut DHIS2 exposes for group→set linkage.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.schemas import OrganisationUnitGroup, OrganisationUnitGroupSet

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client
from dhis2_client.envelopes import WebMessageResponse

_OU_GROUP_SET_FIELDS: str = (
    "id,name,shortName,code,description,compulsory,dataDimension,includeSubhierarchyInAnalytics,"
    "organisationUnitGroups[id,name,code]"
)


class OrganisationUnitGroupSetsAccessor:
    """`Dhis2Client.organisation_unit_group_sets` — CRUD + group-membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[OrganisationUnitGroupSet]:
        """Return every OrganisationUnitGroupSet with its groups resolved inline."""
        raw = await self._client.get_raw(
            "/api/organisationUnitGroupSets",
            params={"fields": _OU_GROUP_SET_FIELDS, "paging": "false"},
        )
        rows = raw.get("organisationUnitGroupSets") or []
        return [OrganisationUnitGroupSet.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> OrganisationUnitGroupSet:
        """Fetch one group set by UID with its `organisationUnitGroups` populated."""
        return await self._client.get(
            f"/api/organisationUnitGroupSets/{uid}",
            model=OrganisationUnitGroupSet,
            params={"fields": _OU_GROUP_SET_FIELDS},
        )

    async def list_groups(self, uid: str) -> list[OrganisationUnitGroup]:
        """Return the groups that belong to one group set, in definition order."""
        group_set = await self.get(uid)
        groups = group_set.organisationUnitGroups or []
        return [OrganisationUnitGroup.model_validate(g) for g in groups if isinstance(g, dict)]

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
        include_subhierarchy_in_analytics: bool = False,
    ) -> OrganisationUnitGroupSet:
        """Create an empty group set; wire groups into it via `add_groups`.

        `data_dimension=True` (the default) exposes the set as an axis
        in the Pivot Table + Data Visualizer apps. `compulsory=True`
        requires every OU to land in exactly one group of the set —
        DHIS2's Data Integrity checks will flag dangling OUs otherwise.
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "compulsory": compulsory,
            "dataDimension": data_dimension,
            "includeSubhierarchyInAnalytics": include_subhierarchy_in_analytics,
        }
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post("/api/organisationUnitGroupSets", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("organisation-unit-group-set create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group_set: OrganisationUnitGroupSet) -> OrganisationUnitGroupSet:
        """PUT an edited group set back. `group_set.id` must be set."""
        if not group_set.id:
            raise ValueError("update requires group_set.id to be set")
        body = group_set.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/organisationUnitGroupSets/{group_set.id}", body=body)
        return await self.get(group_set.id)

    async def add_groups(self, uid: str, *, group_uids: list[str]) -> OrganisationUnitGroupSet:
        """Add `group_uids` to the set via the per-item POST shortcut."""
        for group_uid in group_uids:
            await self._client.resources.organisation_unit_group_sets.add_collection_item(
                uid, "organisationUnitGroups", group_uid
            )
        return await self.get(uid)

    async def remove_groups(self, uid: str, *, group_uids: list[str]) -> OrganisationUnitGroupSet:
        """Drop `group_uids` from the set via the per-item DELETE shortcut."""
        for group_uid in group_uids:
            await self._client.resources.organisation_unit_group_sets.remove_collection_item(
                uid, "organisationUnitGroups", group_uid
            )
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete a group set — groups stay, only the dimension row is removed."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.organisation_unit_group_sets.delete(uid)


__all__ = [
    "OrganisationUnitGroupSet",
    "OrganisationUnitGroupSetsAccessor",
]
