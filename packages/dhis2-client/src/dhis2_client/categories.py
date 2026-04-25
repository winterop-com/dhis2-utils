"""Category authoring — `Dhis2Client.categories`.

A `Category` is one axis of a disaggregation (e.g. `Sex`, `Age group`,
`Modality`). Each Category owns an ordered list of `CategoryOption`s
(the values along that axis). DHIS2 then composes Categories into a
`CategoryCombo` (the disaggregation grid) — and the cross-product of
options across the combo's categories materialises as the
`CategoryOptionCombo` set that data values key on.

This module covers the Category layer. The CategoryOption leaf already
ships in `dhis2_client.category_options`; CategoryCombo + the
auto-generated CategoryOptionCombo matrix are the next layers in the
strategic-option queue.

Generic CRUD stays on the generated accessor
(`client.resources.categories`); this module adds keyword-arg creation
with optional `--options` wiring at create time, partial rename, and
per-item `add_option` / `remove_option` shortcuts that round-trip the
ordered membership via `add_collection_item` /
`remove_collection_item`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.schemas import Category

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client

_CATEGORY_FIELDS: str = "id,name,shortName,code,description,dataDimensionType,dataDimension,categoryOptions[id,name]"


class CategoriesAccessor:
    """`Dhis2Client.categories` — CRUD + rename + per-item option membership helpers."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[Category]:
        """Page through Categories with categoryOptions resolved inline."""
        raw = await self._client.get_raw(
            "/api/categories",
            params={
                "fields": _CATEGORY_FIELDS,
                "page": str(page),
                "pageSize": str(page_size),
            },
        )
        rows = raw.get("categories") or []
        return [Category.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> Category:
        """Fetch one Category by UID."""
        return await self._client.get(f"/api/categories/{uid}", model=Category, params={"fields": _CATEGORY_FIELDS})

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        code: str | None = None,
        description: str | None = None,
        data_dimension_type: str = "DISAGGREGATION",
        options: list[str] | None = None,
        uid: str | None = None,
    ) -> Category:
        """Create a Category, optionally wiring CategoryOption members on create.

        `data_dimension_type` is `DISAGGREGATION` (the default — categories
        that participate in the data-value matrix) or `ATTRIBUTE` (categories
        used for attribute-option-combo metadata only). `options` is an
        ordered list of CategoryOption UIDs; DHIS2 preserves the order on
        save and uses it when materialising the CategoryOptionCombo matrix.
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "dataDimensionType": data_dimension_type,
        }
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        if options:
            payload["categoryOptions"] = [{"id": option_uid} for option_uid in options]
        if uid:
            payload["id"] = uid
        envelope = await self._client.post("/api/categories", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("category create did not return a uid")
        return await self.get(created_uid)

    async def update(self, category: Category) -> Category:
        """PUT an edited Category back. `category.id` must be set."""
        if not category.id:
            raise ValueError("update requires category.id to be set")
        body = category.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/categories/{category.id}", body=body)
        return await self.get(category.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        description: str | None = None,
    ) -> Category:
        """Partial-update the label fields — read, mutate, PUT."""
        if name is None and short_name is None and description is None:
            raise ValueError("rename requires at least one of name / short_name / description")
        current = await self.get(uid)
        if name is not None:
            current.name = name
        if short_name is not None:
            current.shortName = short_name
        if description is not None:
            current.description = description
        return await self.update(current)

    async def add_option(self, uid: str, option_uid: str) -> None:
        """Append a CategoryOption to this Category's ordered membership.

        DHIS2 preserves insertion order on the `categoryOptions` array —
        relevant when the parent CategoryCombo materialises its
        CategoryOptionCombo matrix. To re-order, edit the array via
        `update(category)` directly.
        """
        await self._client.resources.categories.add_collection_item(uid, "categoryOptions", option_uid)

    async def remove_option(self, uid: str, option_uid: str) -> None:
        """Remove a CategoryOption from this Category's membership."""
        await self._client.resources.categories.remove_collection_item(uid, "categoryOptions", option_uid)

    async def delete(self, uid: str) -> None:
        """Delete a Category — DHIS2 rejects deletes on categories referenced by a CategoryCombo."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.categories.delete(uid)


__all__ = [
    "CategoriesAccessor",
    "Category",
]
