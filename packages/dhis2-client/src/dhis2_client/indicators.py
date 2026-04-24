"""Indicator authoring — `Dhis2Client.indicators`.

DHIS2 `Indicator`s are computed ratios / counts / percentages over
DataElement values, identified by a numerator + denominator
expression pair (each referencing DE UIDs via `#{<uid>}` + optional
Category-Option-Combo refs via `.{<coc_uid>}`). Every indicator also
carries an `IndicatorType` reference that pins the output scaling
factor (`COUNT` / `PERCENT` / `PER_100_PEOPLE` / etc).

Generic CRUD lives on the generated accessor (`client.resources.indicators`);
this module adds the authoring + validation primitives typical
workflows reach for:

- `create(...)` — named kwargs for the required subset (name,
  short_name, indicator_type_uid, numerator, denominator) plus the
  optional expression descriptions + legend sets.
- `update(indicator)` — PUT with an existing typed model.
- `rename(uid, ...)` — partial-update shortcut for label fields.
- `validate_expression(expr)` — pre-flight wrapper around
  `client.validation.describe_expression(..., context="indicator")`
  so callers can catch bad refs before attempting a create.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.schemas import Indicator
from dhis2_client.validation import ExpressionDescription

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_INDICATOR_FIELDS: str = (
    "id,name,shortName,code,description,numerator,denominator,numeratorDescription,"
    "denominatorDescription,annualized,decimals,indicatorType[id,name,factor],"
    "legendSets[id,name],indicatorGroups[id,name]"
)


class IndicatorsAccessor:
    """`Dhis2Client.indicators` — CRUD + rename + expression validation."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[Indicator]:
        """Page through Indicators with type + expressions resolved inline."""
        raw = await self._client.get_raw(
            "/api/indicators",
            params={
                "fields": _INDICATOR_FIELDS,
                "page": str(page),
                "pageSize": str(page_size),
            },
        )
        rows = raw.get("indicators") or []
        return [Indicator.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> Indicator:
        """Fetch one Indicator by UID."""
        raw = await self._client.get_raw(
            f"/api/indicators/{uid}",
            params={"fields": _INDICATOR_FIELDS},
        )
        return Indicator.model_validate(raw)

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        indicator_type_uid: str,
        numerator: str,
        denominator: str,
        numerator_description: str | None = None,
        denominator_description: str | None = None,
        legend_set_uids: list[str] | None = None,
        annualized: bool = False,
        decimals: int | None = None,
        code: str | None = None,
        description: str | None = None,
        uid: str | None = None,
    ) -> Indicator:
        """Create an Indicator.

        `indicator_type_uid` pins the output scale (percent / count /
        etc.) via an `IndicatorType` reference. `numerator` and
        `denominator` are DHIS2 expressions — `#{<de_uid>}` for a DE,
        `#{<de_uid>.<coc_uid>}` for a DE × CategoryOptionCombo cell,
        arithmetic operators allowed. Call `validate_expression(expr)`
        first to catch typos before a failed create.
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "indicatorType": {"id": indicator_type_uid},
            "numerator": numerator,
            "denominator": denominator,
            "annualized": annualized,
        }
        if numerator_description:
            payload["numeratorDescription"] = numerator_description
        if denominator_description:
            payload["denominatorDescription"] = denominator_description
        if decimals is not None:
            payload["decimals"] = decimals
        if legend_set_uids:
            payload["legendSets"] = [{"id": uid_} for uid_ in legend_set_uids]
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post_raw("/api/indicators", body=payload)
        created_uid = _uid_from_webmessage(envelope) or uid
        if not created_uid:
            raise RuntimeError("indicator create did not return a uid")
        return await self.get(created_uid)

    async def update(self, indicator: Indicator) -> Indicator:
        """PUT an edited Indicator back. `indicator.id` must be set."""
        if not indicator.id:
            raise ValueError("update requires indicator.id to be set")
        body = indicator.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/indicators/{indicator.id}", body=body)
        return await self.get(indicator.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        description: str | None = None,
    ) -> Indicator:
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

    async def set_legend_sets(self, uid: str, *, legend_set_uids: list[str]) -> Indicator:
        """Replace the legend-set refs on one Indicator."""
        current = await self.get(uid)
        current.legendSets = [Reference(id=ref).model_dump(by_alias=True, exclude_none=True) for ref in legend_set_uids]
        return await self.update(current)

    async def validate_expression(self, expression: str) -> ExpressionDescription:
        """Parse-check a numerator / denominator expression via DHIS2's validator.

        Wraps `client.validation.describe_expression(expression,
        context="indicator")`. Returns the typed
        `ExpressionDescription` — `.status == "OK"` on success,
        `.message` names the failing reference when DHIS2 rejects.
        Cheap pre-flight for create flows that want early error
        feedback instead of a full-object POST rejection.
        """
        return await self._client.validation.describe_expression(expression, context="indicator")

    async def delete(self, uid: str) -> None:
        """Delete an Indicator — DHIS2 rejects deletes on indicators used in viz / dashboards."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.indicators.delete(uid)


def _uid_from_webmessage(envelope: dict[str, Any]) -> str | None:
    """Pull the created UID out of DHIS2's `WebMessage` response envelope."""
    response = envelope.get("response")
    if isinstance(response, dict):
        uid = response.get("uid")
        if isinstance(uid, str):
            return uid
    return None


__all__ = [
    "Indicator",
    "IndicatorsAccessor",
]
