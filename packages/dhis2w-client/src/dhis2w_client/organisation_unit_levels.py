"""OrganisationUnitLevel naming + listing — `Dhis2Client.organisation_unit_levels`.

DHIS2 auto-creates one `OrganisationUnitLevel` row per depth in the
OU tree (level 1 = roots, level 2 = their children, etc.) but leaves
them unnamed until an admin supplies human labels — "Country",
"Province", "District", "Facility". Those labels are what the
Maintenance app + analytics UIs surface in dropdowns, so a freshly
seeded instance with anonymous levels is hard to navigate.

Renaming is the only common write operation. This accessor covers
list / get / rename + the offline-hierarchy tuning knob
(`offline_levels`) instances sometimes use for mobile caching. Full
CRUD (create / delete) is available on the generated accessor
(`client.resources.organisation_unit_levels`) for admins who need it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2w_client.generated.v42.schemas import OrganisationUnitLevel

if TYPE_CHECKING:
    from dhis2w_client.client import Dhis2Client
from dhis2w_client._collection import parse_collection
from dhis2w_client.envelopes import WebMessageResponse

_OU_LEVEL_FIELDS: str = "id,level,name,code,offlineLevels"


class OrganisationUnitLevelsAccessor:
    """`Dhis2Client.organisation_unit_levels` — list / get / rename OU levels."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[OrganisationUnitLevel]:
        """Return every level sorted by `level` ascending (roots first)."""
        raw = await self._client.get_raw(
            "/api/organisationUnitLevels",
            params={
                "fields": _OU_LEVEL_FIELDS,
                "order": "level:asc",
                "paging": "false",
            },
        )
        return parse_collection(raw, "organisationUnitLevels", OrganisationUnitLevel)

    async def list_with_gaps(self) -> list[OrganisationUnitLevel]:
        """Return existing level rows + synthetic placeholders for every OU depth without a row.

        DHIS2 only persists an `OrganisationUnitLevel` row when one is
        explicitly created (via the Maintenance app or this accessor's
        `rename` methods). A freshly-seeded instance typically has rows
        only for the depths a fixture touched, so `list_all()` hides
        the full shape of the tree.

        `list_with_gaps()` fills the missing slots with synthesised
        `OrganisationUnitLevel(level=N, name=None, id=None)` entries so
        CLI/MCP renderers can show `(unnamed)` for every depth the tree
        actually has. Synthetic rows have no `id` — callers that want
        to name one should POST a new row via `/api/organisationUnitLevels`
        (or use the `rename_by_level` method which PUTs to an existing
        row only).
        """
        existing = await self.list_all()
        named_depths = {row.level for row in existing if row.level is not None}
        max_depth = await self._max_tree_depth()
        synthetic: list[OrganisationUnitLevel] = []
        for depth in range(1, max_depth + 1):
            if depth not in named_depths:
                synthetic.append(OrganisationUnitLevel(level=depth, name=None, id=None))
        merged = existing + synthetic
        merged.sort(key=lambda row: row.level or 0)
        return merged

    async def _max_tree_depth(self) -> int:
        """Cheapest way to ask "how deep does the OU tree go?" — one paged GET.

        Hits `/api/organisationUnits?fields=level&order=level:desc&pageSize=1`
        so the server returns exactly one OU — the deepest one. Zero if
        the instance has no OUs (unusual but handled).
        """
        raw = await self._client.get_raw(
            "/api/organisationUnits",
            params={"fields": "level", "order": "level:desc", "pageSize": "1"},
        )
        rows = raw.get("organisationUnits") or []
        if not rows or not isinstance(rows[0], dict):
            return 0
        level = rows[0].get("level")
        return int(level) if isinstance(level, int | str) and str(level).isdigit() else 0

    async def get(self, uid: str) -> OrganisationUnitLevel:
        """Fetch one level row by UID."""
        return await self._client.get(
            f"/api/organisationUnitLevels/{uid}", model=OrganisationUnitLevel, params={"fields": _OU_LEVEL_FIELDS}
        )

    async def get_by_level(self, level: int) -> OrganisationUnitLevel | None:
        """Resolve a level row by its numeric depth (1 = roots)."""
        raw = await self._client.get_raw(
            "/api/organisationUnitLevels",
            params={
                "fields": _OU_LEVEL_FIELDS,
                "filter": f"level:eq:{level}",
                "paging": "false",
            },
        )
        rows = raw.get("organisationUnitLevels") or []
        for row in rows:
            if isinstance(row, dict):
                return OrganisationUnitLevel.model_validate(row)
        return None

    async def rename(
        self,
        uid: str,
        *,
        name: str,
        code: str | None = None,
        offline_levels: int | None = None,
    ) -> OrganisationUnitLevel:
        """Rename a level (and optionally tweak `code` / `offlineLevels`).

        DHIS2 rejects PATCH on this endpoint, so the shape is "GET,
        mutate, PUT". Returns the freshly-fetched level so the caller
        sees the persisted row.
        """
        level = await self.get(uid)
        body = level.model_dump(by_alias=True, exclude_none=True, mode="json")
        body["name"] = name
        if code is not None:
            body["code"] = code
        if offline_levels is not None:
            body["offlineLevels"] = offline_levels
        await self._client.put_raw(f"/api/organisationUnitLevels/{uid}", body=body)
        return await self.get(uid)

    async def rename_by_level(
        self,
        level: int,
        *,
        name: str,
        code: str | None = None,
        offline_levels: int | None = None,
    ) -> OrganisationUnitLevel:
        """Upsert the label for a numeric depth — PUT if a row exists, POST otherwise.

        DHIS2 only persists a level row when one is explicitly created,
        so "rename level 2 to 'Province'" on a fresh instance means
        creating the row, not updating it. This method handles both
        cases transparently so callers don't need to know whether the
        row existed.
        """
        existing = await self.get_by_level(level)
        if existing is not None and existing.id:
            return await self.rename(existing.id, name=name, code=code, offline_levels=offline_levels)
        payload: dict[str, Any] = {"level": level, "name": name}
        if code is not None:
            payload["code"] = code
        if offline_levels is not None:
            payload["offlineLevels"] = offline_levels
        envelope = await self._client.post("/api/organisationUnitLevels", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid
        if created_uid:
            return await self.get(created_uid)
        refetched = await self.get_by_level(level)
        if refetched is None:
            raise RuntimeError(f"failed to create OrganisationUnitLevel at depth {level}")
        return refetched


__all__ = [
    "OrganisationUnitLevel",
    "OrganisationUnitLevelsAccessor",
]
