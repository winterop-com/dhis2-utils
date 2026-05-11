"""CategoryOption authoring — `Dhis2Client.category_options`.

CategoryOptions are the values of a `Category` — e.g. `Male` / `Female`
for a `Sex` category, `<1y` / `1-4y` / `5-14y` / `15+` for an `Age group`
category. DHIS2 combines categories into a `CategoryCombo` (the
disaggregation grid), and the cross-product of category options in a
combo becomes the `CategoryOptionCombo` set that data values key on.

This module covers the CategoryOption layer of that chain; the
Category / CategoryCombo / CategoryOptionCombo plumbing stays a
strategic option on the roadmap — the shallower triples in this PR
are independently useful without committing to the whole
disaggregation authoring surface.

Generic CRUD stays on the generated accessor
(`client.resources.category_options`); this module adds keyword-arg
creation + partial rename + a validity-window helper for
`startDate` / `endDate` (DHIS2 allows a date range that bounds when
the option is usable for data entry).
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from dhis2w_client.generated.v43.schemas import CategoryOption

if TYPE_CHECKING:
    from dhis2w_client.v43.client import Dhis2Client
from dhis2w_client.v43._collection import parse_collection
from dhis2w_client.v43.envelopes import WebMessageResponse

_CO_FIELDS: str = (
    "id,name,shortName,code,description,formName,startDate,endDate,categoryOptionGroups[id,name],categories[id,name]"
)


class CategoryOptionsAccessor:
    """`Dhis2Client.category_options` — CRUD + rename + validity-window helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[CategoryOption]:
        """Page through CategoryOptions with references resolved inline."""
        raw = await self._client.get_raw(
            "/api/categoryOptions",
            params={
                "fields": _CO_FIELDS,
                "page": str(page),
                "pageSize": str(page_size),
            },
        )
        return parse_collection(raw, "categoryOptions", CategoryOption)

    async def get(self, uid: str) -> CategoryOption:
        """Fetch one CategoryOption by UID."""
        return await self._client.get(
            f"/api/categoryOptions/{uid}", model=CategoryOption, params={"fields": _CO_FIELDS}
        )

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        code: str | None = None,
        description: str | None = None,
        form_name: str | None = None,
        start_date: datetime | str | None = None,
        end_date: datetime | str | None = None,
        uid: str | None = None,
    ) -> CategoryOption:
        """Create a CategoryOption.

        `start_date` / `end_date` bound the validity window: DHIS2 rejects
        data-value entry against options whose window doesn't cover the
        period. Pass ISO-8601 strings (`"2024-01-01"`) or `datetime`
        instances; omit for an always-valid option.
        """
        payload: dict[str, Any] = {"name": name, "shortName": short_name}
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        if form_name:
            payload["formName"] = form_name
        if start_date is not None:
            payload["startDate"] = _serialise_date(start_date)
        if end_date is not None:
            payload["endDate"] = _serialise_date(end_date)
        if uid:
            payload["id"] = uid
        envelope = await self._client.post("/api/categoryOptions", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("category-option create did not return a uid")
        return await self.get(created_uid)

    async def update(self, option: CategoryOption) -> CategoryOption:
        """PUT an edited CategoryOption back. `option.id` must be set."""
        if not option.id:
            raise ValueError("update requires option.id to be set")
        body = option.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/categoryOptions/{option.id}", body=body)
        return await self.get(option.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
    ) -> CategoryOption:
        """Partial-update the label fields — read, mutate, PUT."""
        if name is None and short_name is None and form_name is None and description is None:
            raise ValueError("rename requires at least one of name / short_name / form_name / description")
        current = await self.get(uid)
        if name is not None:
            current.name = name
        if short_name is not None:
            current.shortName = short_name
        if form_name is not None:
            current.formName = form_name
        if description is not None:
            current.description = description
        return await self.update(current)

    async def set_validity_window(
        self,
        uid: str,
        *,
        start_date: datetime | str | None,
        end_date: datetime | str | None,
    ) -> CategoryOption:
        """Set the `startDate` / `endDate` validity window on a CategoryOption.

        Pass `None` for either side to clear that bound. DHIS2 treats an
        unset window as "always valid"; a set window rejects data-value
        entry for periods outside it.
        """
        current = await self.get(uid)
        current.startDate = _to_datetime(start_date)
        current.endDate = _to_datetime(end_date)
        return await self.update(current)

    async def delete(self, uid: str) -> None:
        """Delete a CategoryOption — DHIS2 rejects deletes on options in use."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.category_options.delete(uid)


def _serialise_date(value: datetime | str) -> str:
    """Normalise to the ISO-8601 date string DHIS2 accepts on `startDate`/`endDate`."""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return value


def _to_datetime(value: datetime | str | None) -> datetime | None:
    """Coerce `start_date` / `end_date` input to `datetime` for the typed model."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


__all__ = [
    "CategoryOption",
    "CategoryOptionsAccessor",
]
