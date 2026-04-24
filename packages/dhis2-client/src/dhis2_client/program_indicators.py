"""ProgramIndicator authoring — `Dhis2Client.program_indicators`.

ProgramIndicators are computed values over tracker event / enrollment
data (the tracker analogue of aggregate `Indicator`s). Each one carries
a `program` reference, an `analyticsType` (`EVENT` or `ENROLLMENT`),
and two DHIS2 expressions: `expression` (the numerator-shaped
computation) plus an optional `filter` (a boolean predicate that
narrows the event/enrollment set).

Generic CRUD stays on the generated accessor
(`client.resources.program_indicators`); this module adds the
authoring primitives the expression-based shape demands:

- `create(...)` — named kwargs for the minimal required subset
  (`name`, `short_name`, `program_uid`, `expression`,
  `analytics_type`).
- `update(pi)` — PUT with an existing typed model.
- `rename(uid, ...)` — partial-update shortcut for label fields.
- `validate_expression(expr)` — pre-flight wrapper around
  `client.validation.describe_expression(..., context="program-indicator")`
  to catch bad DE / TEA / attribute references before create.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.enums import AnalyticsType
from dhis2_client.generated.v42.schemas import ProgramIndicator
from dhis2_client.validation import ExpressionDescription

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_PI_FIELDS: str = (
    "id,name,shortName,code,description,expression,filter,analyticsType,aggregationType,"
    "program[id,name],decimals,legendSets[id,name],programIndicatorGroups[id,name]"
)


class ProgramIndicatorsAccessor:
    """`Dhis2Client.program_indicators` — CRUD + rename + expression validation."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(
        self,
        *,
        program_uid: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> list[ProgramIndicator]:
        """Page through ProgramIndicators, optionally scoped to one program."""
        params: dict[str, Any] = {
            "fields": _PI_FIELDS,
            "page": str(page),
            "pageSize": str(page_size),
        }
        if program_uid is not None:
            params["filter"] = f"program.id:eq:{program_uid}"
        raw = await self._client.get_raw("/api/programIndicators", params=params)
        rows = raw.get("programIndicators") or []
        return [ProgramIndicator.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> ProgramIndicator:
        """Fetch one ProgramIndicator by UID."""
        return await self._client.get(
            f"/api/programIndicators/{uid}", model=ProgramIndicator, params={"fields": _PI_FIELDS}
        )

    async def create(
        self,
        *,
        name: str,
        short_name: str,
        program_uid: str,
        expression: str,
        analytics_type: AnalyticsType | str = AnalyticsType.EVENT,
        filter_expression: str | None = None,
        description: str | None = None,
        aggregation_type: str | None = None,
        decimals: int | None = None,
        legend_set_uids: list[str] | None = None,
        code: str | None = None,
        uid: str | None = None,
    ) -> ProgramIndicator:
        """Create a ProgramIndicator.

        `program_uid` is required — ProgramIndicators don't stand alone;
        they compute over one program's event / enrollment rows.
        `analytics_type=EVENT` aggregates per event row; `ENROLLMENT`
        aggregates per enrolled tracked entity. `expression` is the
        numerator-shaped DHIS2 expression (uses `#{<de_uid>}` for data
        elements, `A{<tea_uid>}` for tracked-entity attributes, etc.);
        `filter_expression` is an optional boolean predicate that
        narrows the rows the expression runs over. Call
        `validate_expression(expr)` first to catch typos before a
        failed create.
        """
        payload: dict[str, Any] = {
            "name": name,
            "shortName": short_name,
            "program": {"id": program_uid},
            "expression": expression,
            "analyticsType": analytics_type.value if isinstance(analytics_type, AnalyticsType) else analytics_type,
        }
        if filter_expression is not None:
            payload["filter"] = filter_expression
        if description:
            payload["description"] = description
        if aggregation_type:
            payload["aggregationType"] = aggregation_type
        if decimals is not None:
            payload["decimals"] = decimals
        if legend_set_uids:
            payload["legendSets"] = [{"id": uid_} for uid_ in legend_set_uids]
        if code:
            payload["code"] = code
        if uid:
            payload["id"] = uid
        envelope = await self._client.post("/api/programIndicators", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("program-indicator create did not return a uid")
        return await self.get(created_uid)

    async def update(self, pi: ProgramIndicator) -> ProgramIndicator:
        """PUT an edited ProgramIndicator back. `pi.id` must be set."""
        if not pi.id:
            raise ValueError("update requires pi.id to be set")
        body = pi.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/programIndicators/{pi.id}", body=body)
        return await self.get(pi.id)

    async def rename(
        self,
        uid: str,
        *,
        name: str | None = None,
        short_name: str | None = None,
        description: str | None = None,
    ) -> ProgramIndicator:
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

    async def set_legend_sets(self, uid: str, *, legend_set_uids: list[str]) -> ProgramIndicator:
        """Replace the legend-set refs on one ProgramIndicator."""
        current = await self.get(uid)
        current.legendSets = [Reference(id=ref).model_dump(by_alias=True, exclude_none=True) for ref in legend_set_uids]
        return await self.update(current)

    async def validate_expression(self, expression: str) -> ExpressionDescription:
        """Parse-check a program-indicator expression via DHIS2's validator.

        Wraps `client.validation.describe_expression(expression,
        context="program-indicator")`. Returns the typed
        `ExpressionDescription` — `.status == "OK"` on success, `.message`
        names the failing reference when DHIS2 rejects. Cheap pre-flight
        for create flows that want early feedback on DE / TEA UID typos.
        """
        return await self._client.validation.describe_expression(expression, context="program-indicator")

    async def delete(self, uid: str) -> None:
        """Delete a ProgramIndicator — DHIS2 rejects deletes on PIs used in viz / dashboards."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.program_indicators.delete(uid)


__all__ = [
    "ProgramIndicator",
    "ProgramIndicatorsAccessor",
]
