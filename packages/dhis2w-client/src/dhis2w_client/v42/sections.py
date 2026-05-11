"""Section authoring — `Dhis2Client.sections`.

A DHIS2 `Section` groups DataElements inside a DataSet for display in
the Data Entry app. A DataSet can be sectionless (flat list) or ship
multiple sections (monthly supply vs stock-out, ANC vs delivery, …).
Each Section carries an ordered `dataElements[]` reference list plus
optional `indicators[]` for the side pane.

Generic CRUD lives on the generated accessor (`client.resources.sections`);
this module adds the authoring primitives that matter for operators:

- `create(...)` — named kwargs over `name` + parent `data_set_uid` +
  optional `sort_order` / `description` / common toggles.
- `list_for(data_set_uid)` — narrow to one DataSet's sections in sort order.
- `add_element` / `remove_element` / `reorder` — the DE-ordering
  primitives a section-aware authoring flow needs. `reorder` takes a
  full list of DE UIDs and sets `dataElements` to that ordering in
  one PUT.
- `rename(uid, ...)` — partial-update shortcut for label fields.
- `delete(uid)` — removes the section shell; DEs stay on the DataSet.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from dhis2w_client.generated.v42.schemas import Section

if TYPE_CHECKING:
    from dhis2w_client.v42.client import Dhis2Client
from dhis2w_client.v42.envelopes import WebMessageResponse

_SECTION_FIELDS: str = (
    "id,name,code,description,sortOrder,"
    "dataSet[id,name],"
    "dataElements[id,name,code],"
    "indicators[id,name,code],"
    "showColumnTotals,showRowTotals,disableDataElementAutoGroup"
)


class SectionsAccessor:
    """`Dhis2Client.sections` — CRUD + ordering helpers over `/api/sections`."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[Section]:
        """Page through Sections across every DataSet."""
        return cast(
            list[Section],
            await self._client.resources.sections.list(
                fields=_SECTION_FIELDS,
                order=["sortOrder:asc"],
                page=page,
                page_size=page_size,
            ),
        )

    async def list_for(self, data_set_uid: str) -> list[Section]:
        """Return the Sections belonging to one DataSet, in sort order."""
        return cast(
            list[Section],
            await self._client.resources.sections.list(
                fields=_SECTION_FIELDS,
                filters=[f"dataSet.id:eq:{data_set_uid}"],
                order=["sortOrder:asc"],
                paging=False,
            ),
        )

    async def get(self, uid: str) -> Section:
        """Fetch one Section by UID with its DE refs resolved inline."""
        return await self._client.get(f"/api/sections/{uid}", model=Section, params={"fields": _SECTION_FIELDS})

    async def create(
        self,
        *,
        name: str,
        data_set_uid: str,
        sort_order: int | None = None,
        description: str | None = None,
        code: str | None = None,
        data_element_uids: list[str] | None = None,
        indicator_uids: list[str] | None = None,
        show_column_totals: bool | None = None,
        show_row_totals: bool | None = None,
        uid: str | None = None,
    ) -> Section:
        """Create a Section attached to `data_set_uid`.

        `data_element_uids` seeds the ordered DE list. If omitted, the
        section starts empty and DEs can be added with `add_element` or
        `reorder` afterward. `sort_order` controls where the section
        renders in the DataSet; sections are ordered ascending.
        """
        payload: dict[str, Any] = {
            "name": name,
            "dataSet": {"id": data_set_uid},
        }
        if uid:
            payload["id"] = uid
        if sort_order is not None:
            payload["sortOrder"] = sort_order
        if description:
            payload["description"] = description
        if code:
            payload["code"] = code
        if data_element_uids:
            payload["dataElements"] = [{"id": de_uid} for de_uid in data_element_uids]
        if indicator_uids:
            payload["indicators"] = [{"id": ind_uid} for ind_uid in indicator_uids]
        if show_column_totals is not None:
            payload["showColumnTotals"] = show_column_totals
        if show_row_totals is not None:
            payload["showRowTotals"] = show_row_totals
        envelope = await self._client.post("/api/sections", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("section create did not return a uid")
        return await self.get(created_uid)

    async def update(self, section: Section) -> Section:
        """PUT an edited Section back. `section.id` must be set."""
        if not section.id:
            raise ValueError("update requires section.id to be set")
        body = section.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/sections/{section.id}", body=body)
        return await self.get(section.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        description: str | None = None,
        sort_order: int | None = None,
    ) -> Section:
        """Partial-update shortcut — read, mutate label / order, PUT."""
        if name is None and description is None and sort_order is None:
            raise ValueError("rename requires at least one of name / description / sort_order")
        current = await self.get(uid)
        if name is not None:
            current.name = name
        if description is not None:
            current.description = description
        if sort_order is not None:
            current.sortOrder = sort_order
        return await self.update(current)

    async def add_element(
        self,
        section_uid: str,
        data_element_uid: str,
        *,
        position: int | None = None,
    ) -> Section:
        """Append (or insert at `position`) a DataElement to the Section.

        DHIS2 preserves the order of `dataElements[]` for data-entry
        rendering. `position` is 0-indexed; omit to append.
        """
        current = await self.get(section_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        existing_ids = [ref.get("id") for ref in (raw.get("dataElements") or []) if isinstance(ref, dict)]
        if data_element_uid in existing_ids:
            return current
        refs = [{"id": ref_id} for ref_id in existing_ids if ref_id]
        if position is None or position >= len(refs):
            refs.append({"id": data_element_uid})
        else:
            refs.insert(max(position, 0), {"id": data_element_uid})
        raw["dataElements"] = refs
        await self._client.put_raw(f"/api/sections/{section_uid}", body=raw)
        return await self.get(section_uid)

    async def remove_element(self, section_uid: str, data_element_uid: str) -> Section:
        """Remove a DataElement from the Section without touching the DataSet."""
        current = await self.get(section_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        existing_ids = [ref.get("id") for ref in (raw.get("dataElements") or []) if isinstance(ref, dict)]
        filtered = [ref_id for ref_id in existing_ids if ref_id and ref_id != data_element_uid]
        if len(filtered) == len(existing_ids):
            return current
        raw["dataElements"] = [{"id": ref_id} for ref_id in filtered]
        await self._client.put_raw(f"/api/sections/{section_uid}", body=raw)
        return await self.get(section_uid)

    async def reorder(self, section_uid: str, data_element_uids: list[str]) -> Section:
        """Replace the Section's `dataElements` with exactly `data_element_uids`, in order.

        Any DE UID not in the list is dropped from the Section. Missing
        UIDs aren't checked against the parent DataSet here — a
        subsequent render or validation run catches the inconsistency.
        """
        current = await self.get(section_uid)
        raw = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        raw["dataElements"] = [{"id": ref_id} for ref_id in data_element_uids]
        await self._client.put_raw(f"/api/sections/{section_uid}", body=raw)
        return await self.get(section_uid)

    async def delete(self, uid: str) -> None:
        """Delete a Section — DEs stay on the parent DataSet."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.sections.delete(uid)


__all__ = [
    "Section",
    "SectionsAccessor",
]
