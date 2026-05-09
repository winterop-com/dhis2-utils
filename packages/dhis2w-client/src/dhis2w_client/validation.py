"""DHIS2 validation-rule workflow — `Dhis2Client.validation`.

Companion to `client.maintenance` (data-integrity). Validation rules are
boolean formulas over data elements (e.g. `ANC 1st visit >= ANC 4th visit`
logically doesn't hold). Running the rules against captured data produces
violations — cells where the rule evaluates to `false`.

Three endpoint families covered:

- **Ad-hoc analysis** — `POST /api/dataAnalysis/validationRules`. Runs the
  analysis synchronously + returns violations. `persist=True` writes the
  violations into DHIS2's `/api/validationResults` table; `notification=True`
  sends out the configured notification templates.
- **Stored results** — `GET|DELETE /api/validationResults`. Browse / purge
  results previously persisted.
- **Expression validation** — `/api/expressions/description`, plus
  per-context variants (`/api/validationRules/expression/description`,
  `/api/indicators/expression/description`,
  `/api/predictors/expression/description`,
  `/api/programIndicators/expression/description`). Ad-hoc check that an
  expression parses + references existing UIDs.

CRUD for `validationRules` / `predictors` themselves stays on the generated
`client.resources` accessors (`client.resources.validation_rules.save_bulk(...)`
etc.). This module is only for the *workflow* endpoints.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict

from dhis2w_client._collection import parse_collection
from dhis2w_client.envelopes import WebMessageResponse
from dhis2w_client.generated.v42.enums import Importance
from dhis2w_client.generated.v42.oas import ValidationResult

if TYPE_CHECKING:
    from dhis2w_client.client import Dhis2Client


ExpressionContext = Literal["generic", "validation-rule", "indicator", "predictor", "program-indicator"]


class ValidationAnalysisResult(BaseModel):
    """One hit from `POST /api/dataAnalysis/validationRules`.

    Distinct from the persisted `ValidationResult` (stored at
    `/api/validationResults`): the ad-hoc analysis endpoint returns a flat
    shape — IDs + display names inlined — while the persisted shape nests
    full `BaseIdentifiableObject` refs. Both are useful, so we keep both
    models; this one is what `run_analysis()` returns.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    validationRuleId: str | None = None
    validationRuleDescription: str | None = None
    organisationUnitId: str | None = None
    organisationUnitDisplayName: str | None = None
    organisationUnitPath: str | None = None
    organisationUnitAncestorNames: str | None = None
    periodId: str | None = None
    periodDisplayName: str | None = None
    attributeOptionComboId: str | None = None
    attributeOptionComboDisplayName: str | None = None
    importance: Importance | None = None
    leftSideValue: float | None = None
    operator: str | None = None
    rightSideValue: float | None = None


# `/api/validationResults` silently ignores `fields=*` and `fields=:all` — the
# rows come back with id-only nested refs unless you name every property
# explicitly. This default selector makes the list + get responses carry the
# same display-friendly detail the analysis endpoint returns inline, so
# callers get readable rule names + importance + operator without a second
# lookup. See BUGS.md #19 for the upstream quirk.
_DEFAULT_RESULT_FIELDS: str = (
    "id,leftsideValue,rightsideValue,notificationSent,dayInPeriod,created,"
    "validationRule[id,displayName,importance,operator],"
    "organisationUnit[id,displayName],"
    "period[id,displayName],"
    "attributeOptionCombo[id,displayName]"
)


_EXPRESSION_DESCRIBE_PATHS: dict[ExpressionContext, tuple[str, str]] = {
    # Each value is (HTTP method, path). `generic` is GET with `?expression=…`;
    # the per-context variants are POST with the expression as `text/plain`.
    "generic": ("GET", "/api/expressions/description"),
    "validation-rule": ("POST", "/api/validationRules/expression/description"),
    "indicator": ("POST", "/api/indicators/expression/description"),
    "predictor": ("POST", "/api/predictors/expression/description"),
    "program-indicator": ("POST", "/api/programIndicators/expression/description"),
}


class ExpressionDescription(BaseModel):
    """Result of `/api/expressions/description` — parse status + rendered description.

    DHIS2 returns a `WebMessage`-ish envelope with `message="Valid"` on parse
    success and `description="…"` rendering the expression with UIDs replaced
    by names. Errors come back with `status="ERROR"` and a `message` naming
    the problem (e.g. `"Data element not found: abcUid"`).
    """

    model_config = ConfigDict(extra="allow")

    status: str | None = None
    message: str | None = None
    description: str | None = None

    @property
    def valid(self) -> bool:
        """`True` when DHIS2 accepted the expression; `False` on parse errors."""
        return (self.status or "").upper() == "OK"


class ValidationAccessor:
    """`Dhis2Client.validation` — run validation rules + inspect stored results.

    Read the docstrings on individual methods for the DHIS2-endpoint-level
    semantics (persist / notification flags, filter parameters, etc.).
    """

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def run_analysis(
        self,
        *,
        org_unit: str,
        start_date: str,
        end_date: str,
        validation_rule_group: str | None = None,
        max_results: int | None = None,
        notification: bool = False,
        persist: bool = False,
    ) -> list[ValidationAnalysisResult]:
        """Run `POST /api/dataAnalysis/validationRules` synchronously; return violations.

        Synchronous — DHIS2 returns the violations in the response body (no
        task polling). For a whole-instance sweep pass the root org unit UID
        (DHIS2 walks the sub-tree). Narrow with `validation_rule_group` when
        you only want to evaluate one rule bundle.

        `persist=True` writes each violation into DHIS2's
        `/api/validationResults` table so later `list_results()` calls can
        walk them; `notification=True` fires the configured notification
        templates for each triggered rule. Both default off for
        ad-hoc / exploratory runs.
        """
        body: dict[str, Any] = {
            "ou": org_unit,
            "startDate": start_date,
            "endDate": end_date,
            "notification": notification,
            "persist": persist,
        }
        if validation_rule_group is not None:
            body["vrg"] = validation_rule_group
        if max_results is not None:
            body["maxResults"] = max_results
        raw = await self._client.post_raw("/api/dataAnalysis/validationRules", body=body)
        # DHIS2 wraps the list as either `{"data": [...]}` (older v42 builds)
        # or returns the array directly. `_parse_json` wraps top-level arrays
        # as `{"data": [...]}` before this method sees them.
        candidates: list[Any] = []
        data = raw.get("data")
        if isinstance(data, list):
            candidates = data
        else:
            results = raw.get("validationResults")
            if isinstance(results, list):
                candidates = results
        return [ValidationAnalysisResult.model_validate(row) for row in candidates if isinstance(row, dict)]

    async def list_results(
        self,
        *,
        org_unit: str | None = None,
        period: str | None = None,
        validation_rule: str | None = None,
        created_date: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        fields: str | None = None,
    ) -> list[ValidationResult]:
        """List persisted validation results (`GET /api/validationResults`).

        DHIS2 accepts `ou`, `pe`, `vr`, `createdDate` as filters (repeatable
        for `ou`, `pe`, `vr`). Defaults to returning every result — narrow
        with at least one filter on real instances where the table can run
        to millions of rows.

        `fields` defaults to a selector that pulls `displayName` + the
        owning rule's `importance` + `operator` inline, so the resulting
        `ValidationResult`s carry readable data without a second lookup.
        Override with a narrower selector for large-scale runs where only
        counts / UIDs matter.
        """
        params: dict[str, Any] = {"fields": fields if fields is not None else _DEFAULT_RESULT_FIELDS}
        if org_unit is not None:
            params["ou"] = org_unit
        if period is not None:
            params["pe"] = period
        if validation_rule is not None:
            params["vr"] = validation_rule
        if created_date is not None:
            params["createdDate"] = created_date
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size
        raw = await self._client.get_raw("/api/validationResults", params=params)
        return parse_collection(raw, "validationResults", ValidationResult)

    async def get_result(self, result_id: int | str, *, fields: str | None = None) -> ValidationResult:
        """Fetch a single persisted validation result by its numeric id.

        `fields` defaults to the same display-friendly selector
        `list_results` uses — override with a narrower selector if you
        only need a subset.
        """
        params = {"fields": fields if fields is not None else _DEFAULT_RESULT_FIELDS}
        raw = await self._client.get_raw(f"/api/validationResults/{result_id}", params=params)
        return ValidationResult.model_validate(raw)

    async def delete_results(
        self,
        *,
        org_units: Sequence[str] | None = None,
        periods: Sequence[str] | None = None,
        validation_rules: Sequence[str] | None = None,
    ) -> None:
        """Bulk-delete persisted validation results matching the filters.

        `DELETE /api/validationResults` accepts the same filter keys as the
        list endpoint. At least one of `org_units` / `periods` /
        `validation_rules` must be non-empty — a filter-less delete would
        wipe every row.
        """
        if not (org_units or periods or validation_rules):
            raise ValueError(
                "delete_results requires at least one of org_units / periods / validation_rules — "
                "refusing to wipe the whole validation-results table.",
            )
        params: dict[str, list[str]] = {}
        if org_units:
            params["ou"] = list(org_units)
        if periods:
            params["pe"] = list(periods)
        if validation_rules:
            params["vr"] = list(validation_rules)
        await self._client.delete_raw("/api/validationResults", params=params)

    async def send_notifications(self) -> WebMessageResponse:
        """Fire the configured notification templates for every current violation.

        Posts to `/api/validation/sendNotifications` — DHIS2 walks the
        `validationResults` table + queues messages per template.
        """
        raw = await self._client.post_raw("/api/validation/sendNotifications")
        return WebMessageResponse.model_validate(raw)

    async def describe_expression(
        self,
        expression: str,
        *,
        context: ExpressionContext = "generic",
    ) -> ExpressionDescription:
        """Parse-check an expression + render a human description.

        `context` picks which DHIS2 parser runs — `generic` / `validation-rule`
        / `indicator` / `predictor` / `program-indicator` use different
        allowed-reference sets. Returns `ExpressionDescription.valid` (bool)
        + `message` (the parse error, on failure).
        """
        method, path = _EXPRESSION_DESCRIBE_PATHS[context]
        if method == "GET":
            raw = await self._client.get_raw(path, params={"expression": expression})
        else:
            response = await self._client._request(  # noqa: SLF001 — accessor is tight with the client
                "POST",
                path,
                content=expression.encode("utf-8"),
                extra_headers={"Content-Type": "text/plain"},
            )
            raw = response.json() if response.content else {}
        return ExpressionDescription.model_validate(raw)


__all__ = [
    "ExpressionContext",
    "ExpressionDescription",
    "ValidationAccessor",
    "ValidationAnalysisResult",
]
