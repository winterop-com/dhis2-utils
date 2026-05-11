"""Legend set authoring helpers — `Dhis2Client.legend_sets`.

A DHIS2 `LegendSet` is an ordered list of `Legend` objects, each
assigning a colour (hex string) + display name to a half-open numeric
band `[startValue, endValue)`. Visualizations and maps reference a
legend set by UID; at render time DHIS2 buckets each data-value cell
by band and paints it with the matching colour.

Hand-rolling this via `POST /api/metadata` is tedious — ten legends
means ten `Legend` dicts with precomputed UIDs, correct sort order,
and colour validation. `LegendSetSpec` + `LegendSpec` cover the
common case with sensible defaults, generating stable UIDs for each
legend so re-runs of the same spec are idempotent.

## Why POST through `/api/metadata`

Same reason as `Visualization` and `Map`: a direct `PUT
/api/legendSets/{uid}` with nested `legends` works for simple cases
but doesn't round-trip the whole object faithfully (DHIS2 computes
derived fields on the full-metadata path). Route creates + updates
through `POST /api/metadata?importStrategy=CREATE_AND_UPDATE` so both
the LegendSet + its child Legends import atomically.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dhis2w_client.generated.v42.schemas import Legend, LegendSet
from dhis2w_client.v42._collection import parse_collection
from dhis2w_client.v42.envelopes import WebMessageResponse
from dhis2w_client.v42.uids import generate_uid

if TYPE_CHECKING:
    from dhis2w_client.v42.client import Dhis2Client


_LEGEND_SET_FIELDS: str = "id,name,code,symbolizer,created,lastUpdated,legends[id,name,startValue,endValue,color]"


class LegendSpec(BaseModel):
    """Typed builder for one `Legend` inside a `LegendSet` — a `[start, end)` colour range.

    `start` must be strictly less than `end`; the validator enforces
    this. `color` is a CSS-style hex string (`#RRGGBB` or `#RRGGBBAA`);
    anything else DHIS2 renders as the default greyscale. `name`
    defaults to the legend's numeric range when omitted, matching
    DHIS2's own auto-naming in the legend editor.
    """

    model_config = ConfigDict(frozen=True)

    start: float
    end: float
    color: str = Field(description="Hex colour — `#RRGGBB` or `#RRGGBBAA`.")
    name: str | None = None

    @field_validator("end")
    @classmethod
    def _end_must_exceed_start(cls, end: float, info: Any) -> float:
        """Reject legends where `end <= start` — they produce an empty interval."""
        start = info.data.get("start")
        if start is not None and end <= start:
            raise ValueError(f"legend end ({end}) must be strictly greater than start ({start})")
        return end


class LegendSetSpec(BaseModel):
    """Typed builder for a `LegendSet` — name + ordered list of `Legend` entries.

    `uid` is optional; an 11-char UID is generated when omitted. Each
    child legend also gets a stable auto-generated UID so re-runs of
    the same spec (same `uid`, same legend order) upsert without
    creating duplicates.

    Legends are expected in ascending order of `start`; they're kept
    as-given (no implicit sort) so a spec with overlapping or
    non-monotonic legends lands on DHIS2 verbatim and fails at render
    time — that's a user-authored mistake the builder doesn't mask.
    """

    model_config = ConfigDict(frozen=True)

    uid: str | None = None
    name: str
    code: str | None = None
    legends: list[LegendSpec]

    def build(self) -> LegendSet:
        """Materialise the spec into a typed `LegendSet` with inline `Legend` children.

        DHIS2's `/api/metadata` importer for LegendSets requires every
        Legend to be inlined under `legendSets[*].legends[]` as a full
        object with `startValue` / `endValue` / `name` / `color` —
        passing `legends` as a sibling collection of references is
        rejected with `E4000` ("Missing required property") because
        the server-side importer doesn't cross-link references back
        into the parent.
        """
        set_uid = self.uid or generate_uid()
        inline_legends: list[dict[str, Any]] = []
        for legend in self.legends:
            inline_legends.append(
                Legend(
                    id=generate_uid(),
                    name=legend.name or f"{legend.start:g} – {legend.end:g}",
                    startValue=legend.start,
                    endValue=legend.end,
                    color=legend.color,
                ).model_dump(by_alias=True, exclude_none=True, mode="json"),
            )
        return LegendSet(
            id=set_uid,
            name=self.name,
            code=self.code,
            legends=inline_legends,
        )


class LegendSetsAccessor:
    """`Dhis2Client.legend_sets` — list / get / create / clone / delete legend sets."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[LegendSet]:
        """Return every LegendSet with its legends resolved inline."""
        raw = await self._client.get_raw(
            "/api/legendSets",
            params={"fields": _LEGEND_SET_FIELDS, "paging": "false"},
        )
        return parse_collection(raw, "legendSets", LegendSet)

    async def get(self, uid: str) -> LegendSet:
        """Fetch one LegendSet by UID with its `legends` child list resolved inline."""
        raw = await self._client.get_raw(
            f"/api/legendSets/{uid}",
            params={"fields": _LEGEND_SET_FIELDS},
        )
        return LegendSet.model_validate(raw)

    async def create_from_spec(self, spec: LegendSetSpec) -> LegendSet:
        """Build + POST a LegendSet via `/api/metadata` with inline Legend children.

        Returns the freshly-fetched `LegendSet` so the caller sees
        DHIS2's computed fields (`href`, `displayName`, …) populated.
        """
        legend_set = spec.build()
        bundle = {
            "legendSets": [legend_set.model_dump(by_alias=True, exclude_none=True, mode="json")],
        }
        raw = await self._client.post_raw(
            "/api/metadata",
            body=bundle,
            params={"importStrategy": "CREATE_AND_UPDATE", "atomicMode": "OBJECT"},
        )
        envelope = WebMessageResponse.model_validate(raw)
        if envelope.status and envelope.status.upper() not in ("OK", "SUCCESS"):
            raise RuntimeError(
                f"legend-set import failed: status={envelope.status}  message={envelope.message!r}",
            )
        if legend_set.id is None:
            raise RuntimeError("legend set is missing an id after import — cannot fetch back")
        return await self.get(legend_set.id)

    async def clone(
        self,
        source_uid: str,
        *,
        new_uid: str | None = None,
        new_name: str | None = None,
        new_code: str | None = None,
    ) -> LegendSet:
        """Duplicate an existing LegendSet — same legends, fresh UIDs on the set and each legend.

        Useful for forking a base set ("Coverage 0-100") into a variant
        with tweaked colours ("Coverage 0-100 monochrome") without
        rebuilding the legends by hand.
        """
        source = await self.get(source_uid)
        legends_list = source.legends or []
        legend_specs: list[LegendSpec] = []
        for legend in legends_list:
            if not isinstance(legend, dict):
                # Referenced-only legend (no inline payload) — skip rather than fail;
                # DHIS2's `/legendSets/{uid}?fields=legends[...]` always inlines on v42.
                continue
            start = legend.get("startValue")
            end = legend.get("endValue")
            color = legend.get("color")
            if start is None or end is None or not isinstance(color, str):
                continue
            legend_specs.append(
                LegendSpec(
                    start=float(start),
                    end=float(end),
                    color=color,
                    name=legend.get("name") if isinstance(legend.get("name"), str) else None,
                ),
            )
        spec = LegendSetSpec(
            uid=new_uid,
            name=new_name or f"{source.name or 'LegendSet'} (clone)",
            code=new_code,
            legends=legend_specs,
        )
        return await self.create_from_spec(spec)

    async def delete(self, uid: str) -> None:
        """Delete a LegendSet — `DELETE /api/legendSets/{uid}`."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.legend_sets.delete(uid)


__all__ = [
    "Legend",
    "LegendSet",
    "LegendSetSpec",
    "LegendSetsAccessor",
    "LegendSpec",
]
