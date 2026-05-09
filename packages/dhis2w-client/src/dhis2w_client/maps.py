"""Map authoring helpers — `Dhis2Client.maps`.

A DHIS2 `Map` is a geographic-visualization container — a viewport
(longitude, latitude, zoom, basemap) plus an ordered list of
`MapView` layers rendered bottom-up. Each layer is either:

- **THEMATIC** (`layer="thematic"`) — choropleth (one fill colour per
  org unit, driven by a data dimension) or graduated symbols (size
  scales with the value). The most common layer type.
- **BOUNDARY** (`layer="boundary"`) — outline-only layer, typically
  used as a base below thematics.
- **FACILITY** (`layer="facility"`) — point markers for facility-level
  org units.
- **EARTH_ENGINE** / **EVENT** / **ORG_UNIT** — rarer layer types;
  supported via raw `MapView` construction.

Most day-to-day authoring only touches the thematic case: one data
element × one period × one org-unit level → a choropleth of Sierra
Leone's districts coloured by immunization coverage, say.
`MapLayerSpec` + `MapSpec` cover that case with sensible defaults;
drop to the generated `Map` / `MapView` models when you need the
full knob set.

## Why always POST through `/api/metadata`

Same reason as `Visualization`: a direct `PUT /api/maps/{uid}` with
nested `mapViews` silently drops the derived `rows` / `columns` /
`filters` collections DHIS2 renders from. Route creates + updates
through `POST /api/metadata?importStrategy=CREATE_AND_UPDATE` so the
importer expands every dimension selector into the axes DHIS2 reads
at render time. `MapsAccessor.create_from_spec` takes that path.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from dhis2w_client._collection import parse_collection
from dhis2w_client.envelopes import WebMessageResponse
from dhis2w_client.generated.v42.enums import (
    OrganisationUnitSelectionMode,
    ThematicMapType,
)
from dhis2w_client.generated.v42.schemas import Map, MapView
from dhis2w_client.uids import generate_uid

if TYPE_CHECKING:
    from dhis2w_client.client import Dhis2Client


_MAP_FIELDS: str = (
    "id,name,description,title,longitude,latitude,zoom,basemap,created,lastUpdated,"
    "mapViews[id,name,layer,thematicMapType,classes,colorLow,colorHigh,"
    "opacity,aggregationType,renderingStrategy,organisationUnitSelectionMode,"
    "dataDimensionItems[dataDimensionItemType,dataElement[id,name],"
    "indicator[id,name],programIndicator[id,name]],"
    "periods[id],organisationUnits[id,name],organisationUnitLevels]"
)


LayerKind = Literal["thematic", "boundary", "facility"]


class MapLayerSpec(BaseModel):
    """Typed builder for one `MapView` layer on a `Map`.

    Covers the common thematic-choropleth case with sensible defaults.
    Drop down to a raw `MapView` payload for the full knob surface
    (event layers, earth-engine, custom rendering strategies).
    """

    model_config = ConfigDict(frozen=True)

    layer_kind: LayerKind = "thematic"
    data_elements: list[str] = Field(default_factory=list)
    indicators: list[str] = Field(default_factory=list)
    periods: list[str] = Field(default_factory=list)
    organisation_units: list[str] = Field(default_factory=list)
    organisation_unit_levels: list[int] = Field(default_factory=list)
    organisation_unit_selection_mode: OrganisationUnitSelectionMode = OrganisationUnitSelectionMode.SELECTED
    thematic_map_type: ThematicMapType = ThematicMapType.CHOROPLETH
    classes: int = Field(default=5, ge=2, le=9)
    color_low: str = "#fef0d9"
    color_high: str = "#b30000"
    opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    name: str | None = None
    legend_set: str | None = None

    def to_map_view(self) -> MapView:
        """Materialise this layer as a typed `MapView` the metadata importer accepts."""
        base: dict[str, Any] = {
            "layer": self.layer_kind,
            "opacity": self.opacity,
            "organisationUnits": [{"id": ou} for ou in self.organisation_units],
            "organisationUnitLevels": list(self.organisation_unit_levels),
            "organisationUnitSelectionMode": self.organisation_unit_selection_mode.value,
        }
        if self.name is not None:
            base["name"] = self.name
        if self.layer_kind == "thematic":
            data_dimension_items: list[dict[str, Any]] = [
                {"dataDimensionItemType": "DATA_ELEMENT", "dataElement": {"id": uid}} for uid in self.data_elements
            ]
            data_dimension_items.extend(
                {"dataDimensionItemType": "INDICATOR", "indicator": {"id": uid}} for uid in self.indicators
            )
            base.update(
                {
                    "thematicMapType": self.thematic_map_type.value,
                    "classes": self.classes,
                    "colorLow": self.color_low,
                    "colorHigh": self.color_high,
                    "dataDimensionItems": data_dimension_items,
                    "periods": [{"id": pe} for pe in self.periods],
                    "rowDimensions": ["ou"],
                    "columnDimensions": ["dx"],
                    "filterDimensions": ["pe"],
                },
            )
            if self.legend_set is not None:
                base["legendSet"] = {"id": self.legend_set}
        return MapView.model_validate(base)


class MapSpec(BaseModel):
    """Typed builder for a full `Map` — viewport + ordered layers."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=230)
    description: str | None = None
    uid: str | None = None
    title: str | None = None
    longitude: float = Field(default=0.0, ge=-180.0, le=180.0)
    latitude: float = Field(default=0.0, ge=-90.0, le=90.0)
    zoom: int = Field(default=4, ge=0, le=20)
    basemap: str = "openStreetMap"
    layers: list[MapLayerSpec] = Field(..., min_length=1)

    def to_map(self) -> Map:
        """Materialise the typed `Map` DHIS2's metadata importer accepts."""
        map_views: list[dict[str, Any]] = [
            layer.to_map_view().model_dump(by_alias=True, exclude_none=True, mode="json") for layer in self.layers
        ]
        return Map.model_validate(
            {
                "id": self.uid or generate_uid(),
                "name": self.name,
                "description": self.description,
                "title": self.title,
                "longitude": self.longitude,
                "latitude": self.latitude,
                "zoom": self.zoom,
                "basemap": self.basemap,
                "mapViews": map_views,
            },
        )


class MapsAccessor:
    """`Dhis2Client.maps` — workflow helpers over `/api/maps`."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[Map]:
        """List every Map on the instance, sorted by name."""
        raw = await self._client.get_raw(
            "/api/maps",
            params={"fields": "id,name,description,zoom,lastUpdated", "order": "name:asc", "paging": "false"},
        )
        return parse_collection(raw, "maps", Map)

    async def get(self, uid: str) -> Map:
        """Fetch one Map with every `mapViews` layer resolved inline."""
        raw = await self._client.get_raw(f"/api/maps/{uid}", params={"fields": _MAP_FIELDS})
        return Map.model_validate(raw)

    async def create_from_spec(self, spec: MapSpec) -> Map:
        """Build a Map from a spec and POST via `/api/metadata`.

        Route through the metadata importer so derived axes populate.
        A direct `PUT /api/maps/{uid}` with nested `mapViews` silently
        drops `rows` / `columns` / `filters` — don't take that shortcut.
        """
        m = spec.to_map()
        if m.id is None:
            raise ValueError("MapSpec did not assign a UID — check to_map()")
        body = {"maps": [m.model_dump(by_alias=True, exclude_none=True, mode="json")]}
        await self._client.post(
            "/api/metadata",
            body,
            params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL"},
            model=WebMessageResponse,
        )
        return await self.get(m.id)

    async def clone(
        self,
        source_uid: str,
        *,
        new_name: str,
        new_uid: str | None = None,
        new_description: str | None = None,
    ) -> Map:
        """Duplicate an existing Map with a fresh UID + new name.

        Copies the viewport + every layer so the clone renders
        identically. Stripped fields: server-owned (`created`,
        `lastUpdated`, `createdBy`, `lastUpdatedBy`) and display-computed
        shortcuts. `mapViews` carry over with fresh UIDs assigned by
        the importer.
        """
        source = await self.get(source_uid)
        target_uid = new_uid or generate_uid()
        payload = source.model_dump(by_alias=True, exclude_none=True, mode="json")
        for owned in (
            "id",
            "uid",
            "created",
            "lastUpdated",
            "createdBy",
            "lastUpdatedBy",
            "href",
            "access",
            "user",
            "favorites",
            "favorite",
            "subscribers",
            "subscribed",
            "interpretations",
            "displayName",
            "displayDescription",
            "displayFormName",
            "displayShortName",
            "translations",
        ):
            payload.pop(owned, None)
        payload["id"] = target_uid
        payload["name"] = new_name
        if new_description is not None:
            payload["description"] = new_description
        # Strip nested MapView UIDs so the importer mints fresh ones
        # (keeping the source's UIDs would collide on any re-import).
        nested_views = payload.get("mapViews") or []
        scrubbed_views: list[dict[str, Any]] = []
        for view in nested_views:
            if isinstance(view, dict):
                copy = {k: v for k, v in view.items() if k not in ("id", "uid", "created", "lastUpdated")}
                scrubbed_views.append(copy)
        payload["mapViews"] = scrubbed_views
        await self._client.post(
            "/api/metadata",
            {"maps": [payload]},
            params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "ALL"},
            model=WebMessageResponse,
        )
        return await self.get(target_uid)

    async def delete(self, uid: str) -> None:
        """DELETE a Map by UID."""
        await self._client.resources.maps.delete(uid)


__all__ = [
    "LayerKind",
    "MapLayerSpec",
    "MapSpec",
    "MapsAccessor",
]
