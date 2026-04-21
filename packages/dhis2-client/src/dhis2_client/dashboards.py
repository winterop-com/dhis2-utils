"""Dashboard assembly helpers — `Dhis2Client.dashboards`.

DHIS2 `Dashboard` carries an ordered list of `DashboardItem`s, each
slotted on a 60-unit-wide grid via explicit `x / y / width / height`.
The generated CRUD accessor (`client.resources.dashboards`) covers
basic lifecycle — this module layers workflow helpers that the
dashboard app's UI exposes but the raw API forces callers to hand-roll:

- `add_item(dashboard_uid, viz_uid, ...)` — append one visualization
  item to an existing dashboard, read-modify-write against
  `/api/metadata`. Auto-stacks below existing items when `y` is
  omitted.
- `DashboardSlot` — typed x/y/width/height bundle; passed through to
  `add_item` when the caller wants explicit placement.

The "auto-stack below existing" heuristic scans the dashboard's
current items, finds the largest `y + height`, and drops the new item
at that `y`. Callers who want tiling layouts (two charts side-by-side)
set `x` + `width` explicitly and share a `y`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.enums import DashboardItemShape, DashboardItemType
from dhis2_client.generated.v42.schemas import Dashboard, DashboardItem
from dhis2_client.uids import generate_uid

DashboardItemKind = Literal["visualization", "map", "eventVisualization", "eventChart", "eventReport"]

# Mapping from accessor-level kind names to DHIS2's DashboardItem reference
# fields + item-type enum values. DashboardItemKind is limited to the
# "wraps a metadata object" cases — text / message / app items need
# bespoke shapes and bypass this helper.
_KIND_MAP: dict[str, tuple[str, DashboardItemType]] = {
    "visualization": ("visualization", DashboardItemType.VISUALIZATION),
    "map": ("map", DashboardItemType.MAP),
    "eventVisualization": ("eventVisualization", DashboardItemType.EVENT_VISUALIZATION),
    "eventChart": ("eventChart", DashboardItemType.EVENT_CHART),
    "eventReport": ("eventReport", DashboardItemType.EVENT_REPORT),
}

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_DASHBOARD_FIELDS: str = (
    "id,name,description,created,lastUpdated,"
    "dashboardItems[id,type,x,y,width,height,shape,"
    "visualization[id,name,type],map[id,name],eventChart[id,name],"
    "eventVisualization[id,name],eventReport[id,name],reports[id,name],"
    "resources[id,name],users[id,displayName],messages,text]"
)


class DashboardSlot(BaseModel):
    """Grid placement for one dashboard item — x/y/width/height + shape.

    The DHIS2 grid is 60 units wide; heights stack freely. Use `NORMAL`
    shape for blocks that sit alongside neighbours, `FULL_WIDTH` when
    the item spans the entire row and nothing else shares its row, and
    `DOUBLE_WIDTH` for 2-column layouts. The shape is rendering metadata
    — actual layout comes from `width` + `x`.
    """

    model_config = ConfigDict(frozen=True)

    x: int = Field(default=0, ge=0, le=60)
    y: int = Field(default=0, ge=0)
    width: int = Field(default=60, ge=1, le=60)
    height: int = Field(default=20, ge=1)
    shape: DashboardItemShape = DashboardItemShape.NORMAL


class DashboardsAccessor:
    """`Dhis2Client.dashboards` — compose dashboards from existing visualizations."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def get(self, uid: str) -> Dashboard:
        """Fetch one Dashboard with every item + its referenced resource."""
        raw = await self._client.get_raw(f"/api/dashboards/{uid}", params={"fields": _DASHBOARD_FIELDS})
        return Dashboard.model_validate(raw)

    async def list_all(self) -> list[Dashboard]:
        """List every Dashboard on the instance, sorted by name."""
        raw = await self._client.get_raw(
            "/api/dashboards",
            params={"fields": "id,name,description,lastUpdated", "order": "name:asc", "paging": "false"},
        )
        rows = raw.get("dashboards")
        if not isinstance(rows, list):
            return []
        return [Dashboard.model_validate(row) for row in rows if isinstance(row, dict)]

    async def add_item(
        self,
        dashboard_uid: str,
        target_uid: str,
        *,
        kind: DashboardItemKind = "visualization",
        slot: DashboardSlot | None = None,
        item_uid: str | None = None,
    ) -> Dashboard:
        """Append one metadata-backed item (viz / map / event chart / …) to a dashboard.

        `kind` picks which DHIS2 DashboardItem reference field carries
        the UID — `"visualization"` (default), `"map"`,
        `"eventVisualization"`, `"eventChart"`, `"eventReport"`. The
        `type` enum on the item is set automatically from `kind`.

        When `slot` is omitted the new item stacks below every existing
        item: `y` is computed as `max(existing.y + existing.height)` so
        nothing overlaps. Supply a `DashboardSlot` when you need
        side-by-side tiling (share `y`, split `x` + `width`).

        Returns the full updated Dashboard. The PUT uses `/api/metadata`
        to route through the same importer the UI does, so derived
        fields populate correctly.
        """
        if kind not in _KIND_MAP:
            raise ValueError(f"unknown dashboard item kind {kind!r}; expected one of {list(_KIND_MAP)}")
        ref_field, item_type = _KIND_MAP[kind]
        current = await self.get(dashboard_uid)
        existing_items = list(current.dashboardItems or [])
        placement = slot or _auto_stack_below(existing_items)
        item = DashboardItem.model_validate(
            {
                "id": item_uid or generate_uid(),
                "type": item_type.value,
                ref_field: {"id": target_uid},
                "x": placement.x,
                "y": placement.y,
                "width": placement.width,
                "height": placement.height,
                "shape": placement.shape.value,
            },
        )
        updated_items: list[Any] = []
        for entry in existing_items:
            if isinstance(entry, DashboardItem):
                updated_items.append(entry.model_dump(by_alias=True, exclude_none=True, mode="json"))
            elif isinstance(entry, dict):
                updated_items.append(entry)
        updated_items.append(item.model_dump(by_alias=True, exclude_none=True, mode="json"))
        payload = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        # Strip read-only / server-owned fields so the metadata importer
        # treats this as a straight update of the same dashboard.
        for owned in (
            "created",
            "lastUpdated",
            "createdBy",
            "lastUpdatedBy",
            "href",
            "access",
            "user",
            "favorites",
            "favorite",
            "displayName",
            "displayDescription",
        ):
            payload.pop(owned, None)
        payload["dashboardItems"] = updated_items
        raw = await self._client.post_raw(
            "/api/metadata",
            {"dashboards": [payload]},
            params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL"},
        )
        WebMessageResponse.model_validate(raw)
        return await self.get(dashboard_uid)

    async def remove_item(self, dashboard_uid: str, item_uid: str) -> Dashboard:
        """Remove one dashboardItem by its UID and PUT the dashboard back."""
        current = await self.get(dashboard_uid)
        kept: list[Any] = []
        for entry in current.dashboardItems or []:
            entry_uid = (
                entry.id if isinstance(entry, DashboardItem) else entry.get("id") if isinstance(entry, dict) else None
            )
            if entry_uid == item_uid:
                continue
            if isinstance(entry, DashboardItem):
                kept.append(entry.model_dump(by_alias=True, exclude_none=True, mode="json"))
            elif isinstance(entry, dict):
                kept.append(entry)
        payload = current.model_dump(by_alias=True, exclude_none=True, mode="json")
        for owned in (
            "created",
            "lastUpdated",
            "createdBy",
            "lastUpdatedBy",
            "href",
            "access",
            "user",
            "favorites",
            "favorite",
            "displayName",
            "displayDescription",
        ):
            payload.pop(owned, None)
        payload["dashboardItems"] = kept
        raw = await self._client.post_raw(
            "/api/metadata",
            {"dashboards": [payload]},
            params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL"},
        )
        WebMessageResponse.model_validate(raw)
        return await self.get(dashboard_uid)


def _auto_stack_below(existing_items: list[Any]) -> DashboardSlot:
    """Compute a default slot that stacks below every existing item."""
    max_bottom = 0
    for entry in existing_items:
        y = _pluck_int(entry, "y", default=0)
        height = _pluck_int(entry, "height", default=20)
        bottom = y + height
        if bottom > max_bottom:
            max_bottom = bottom
    return DashboardSlot(x=0, y=max_bottom, width=60, height=20, shape=DashboardItemShape.FULL_WIDTH)


def _pluck_int(entry: Any, field: str, *, default: int) -> int:
    """Pull an int-valued attribute from a DashboardItem or dict."""
    value = entry.get(field) if isinstance(entry, dict) else getattr(entry, field, None)
    return int(value) if isinstance(value, int) else default


__all__ = [
    "DashboardItemKind",
    "DashboardSlot",
    "DashboardsAccessor",
]
