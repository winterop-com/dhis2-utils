"""OrganisationUnit authoring + tree navigation — `Dhis2Client.organisation_units`.

DHIS2 models its geographic hierarchy as a single tree of
`OrganisationUnit` rows: every non-root unit carries a `parent`
reference + a materialised `path` string (`/<root>/<child>/...`).
Generic CRUD lives on the generated accessor
(`client.resources.organisation_units`); this module adds the
workflow primitives the tree shape demands but the bare CRUD can't
express in one call:

- Walk a subtree at a bounded depth (`list_descendants`) without
  fetching every OU on the instance.
- Enumerate OUs at a given `level` across the whole tree.
- Reparent a unit via `move(uid, new_parent_uid)` — turns into a full
  PUT of the OU with the parent ref swapped; DHIS2 rebuilds `path`
  server-side on save.
- `create_under(parent_uid, ...)` — fills in the parent + opening-date
  defaults so callers don't hand-roll the reference payload.

All reads return typed `OrganisationUnit` instances; writes go through
the raw client helpers so the caller sees DHIS2's computed fields
(`path`, `hierarchyLevel`, `leaf`, …) on the returned model.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.schemas import OrganisationUnit

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_OU_FIELDS: str = (
    "id,name,shortName,code,level,path,parent[id,name],openingDate,closedDate,leaf,hierarchyLevel,description"
)


class OrganisationUnitsAccessor:
    """`Dhis2Client.organisation_units` — tree-aware reads + authoring helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        level: int | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> list[OrganisationUnit]:
        """List OUs page-by-page, optionally filtered to one `level`.

        Use `level=1` to enumerate top-level roots; higher levels for
        countries / regions / facilities depending on the instance's
        hierarchy depth. Paging is server-side — callers that need every
        row should loop over `page` until the returned list is shorter
        than `page_size`.
        """
        params: dict[str, Any] = {
            "fields": _OU_FIELDS,
            "page": str(page),
            "pageSize": str(page_size),
        }
        if level is not None:
            params["filter"] = f"level:eq:{level}"
        raw = await self._client.get_raw("/api/organisationUnits", params=params)
        rows = raw.get("organisationUnits") or []
        return [OrganisationUnit.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> OrganisationUnit:
        """Fetch one OU by UID with parent + hierarchy fields populated."""
        return await self._client.get(
            f"/api/organisationUnits/{uid}", model=OrganisationUnit, params={"fields": _OU_FIELDS}
        )

    async def list_children(self, parent_uid: str) -> list[OrganisationUnit]:
        """Direct children of one OU, sorted by name.

        One-level walk — used by CLI tree renderers and by analytics
        pickers that show a lazy drill-down. For the whole subtree use
        `list_descendants` with a bounded depth.
        """
        raw = await self._client.get_raw(
            "/api/organisationUnits",
            params={
                "fields": _OU_FIELDS,
                "filter": f"parent.id:eq:{parent_uid}",
                "order": "name:asc",
                "paging": "false",
            },
        )
        rows = raw.get("organisationUnits") or []
        return [OrganisationUnit.model_validate(row) for row in rows if isinstance(row, dict)]

    async def list_descendants(
        self,
        root_uid: str,
        *,
        max_depth: int = 3,
    ) -> list[OrganisationUnit]:
        """Walk a subtree at a bounded depth; include the root itself.

        Breadth-first: emits the root, then every direct child, then
        grandchildren, up to `max_depth` extra levels. Callers rendering
        a tree can group by `hierarchyLevel` to get canonical
        top-to-bottom ordering.
        """
        if max_depth < 0:
            raise ValueError("max_depth must be >= 0")
        root = await self.get(root_uid)
        collected: list[OrganisationUnit] = [root]
        frontier = [root_uid]
        for _depth in range(max_depth):
            if not frontier:
                break
            next_frontier: list[str] = []
            for parent_uid in frontier:
                children = await self.list_children(parent_uid)
                for child in children:
                    collected.append(child)
                    if child.id:
                        next_frontier.append(child.id)
            frontier = next_frontier
        return collected

    async def list_by_level(self, level: int) -> list[OrganisationUnit]:
        """Every OU at a given level — all provinces, all districts, etc.

        Convenience over `list_all(level=..., paging=false)`; sorts by
        `path` so parent/child ordering is stable for reports.
        """
        raw = await self._client.get_raw(
            "/api/organisationUnits",
            params={
                "fields": _OU_FIELDS,
                "filter": f"level:eq:{level}",
                "order": "path:asc",
                "paging": "false",
            },
        )
        rows = raw.get("organisationUnits") or []
        return [OrganisationUnit.model_validate(row) for row in rows if isinstance(row, dict)]

    async def create_under(
        self,
        parent_uid: str,
        *,
        name: str,
        short_name: str,
        opening_date: datetime | str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> OrganisationUnit:
        """Create an OU as a child of `parent_uid`.

        DHIS2 requires `openingDate` on every OU (even an ISO-8601 date
        string works). `short_name` must be <=50 chars; DHIS2 rejects
        longer values. Returns the freshly-fetched OU so the caller sees
        `path` + `hierarchyLevel` populated by the server.
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "openingDate": _serialise_date(opening_date),
            "parent": {"id": parent_uid},
        }
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        created = await self._client.post("/api/organisationUnits", payload, model=WebMessageResponse)
        created_uid = created.created_uid or uid
        if not created_uid:
            raise RuntimeError("organisation-unit create did not return a uid")
        return await self.get(created_uid)

    async def update(self, unit: OrganisationUnit) -> OrganisationUnit:
        """PUT an edited OU back — use after mutating `name`, `description`, etc.

        `unit.id` must be set. DHIS2 recomputes `path` + `hierarchyLevel`
        on the server so the returned model is the authoritative view.
        """
        if not unit.id:
            raise ValueError("update requires unit.id to be set")
        body = unit.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/organisationUnits/{unit.id}", body=body)
        return await self.get(unit.id)

    async def move(self, uid: str, new_parent_uid: str) -> OrganisationUnit:
        """Reparent one OU. DHIS2 rebuilds `path` + `hierarchyLevel` server-side.

        Implemented as a full PUT of the OU with `parent` swapped — the
        JSON-Patch path on DHIS2 v42 doesn't update the cached
        `path`/`hierarchyLevel` derived columns, so a full PUT is the
        safer shape.
        """
        unit = await self.get(uid)
        unit.parent = Reference(id=new_parent_uid)
        return await self.update(unit)

    async def delete(self, uid: str) -> None:
        """Delete an OU. DHIS2 rejects deletes on units with children or data."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.organisation_units.delete(uid)


def _serialise_date(value: datetime | str) -> str:
    """Normalise openingDate to the ISO-8601 string DHIS2 expects."""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return value


__all__ = [
    "OrganisationUnit",
    "OrganisationUnitsAccessor",
]
