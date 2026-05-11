"""Typed models + client accessor for DHIS2 maintenance + data-integrity + task-notification APIs.

`DataIntegrityCheck` and `DataIntegrityIssue` come from
`dhis2w_client.generated.v43.oas`. `DataIntegrityResult` and
`DataIntegrityReport` stay hand-written — OpenAPI splits the result into
separate `DataIntegrityDetails` / `DataIntegritySummary` shapes, but this
module's callers want the merged view + the client-side `{check_name: result}`
map. `Notification` re-exports the OAS type so callers get typed
`category: JobType`, `dataType: NotificationDataType`, `level: NotificationLevel`
enums + `time: datetime`.

`MaintenanceAccessor` (bound to `Dhis2Client.maintenance`) exposes the
data-integrity read paths. `iter_integrity_issues` is the ergonomic
entry point for large runs — yields one issue at a time tagged with its
owning check's metadata, so callers don't have to walk the
`{check_name: {issues: [...]}}` two-level shape themselves.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Sequence
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

from dhis2w_client.generated.v43.oas import DataIntegrityCheck, DataIntegrityIssue, Notification
from dhis2w_client.generated.v43.oas._enums import JobType, NotificationDataType, NotificationLevel

if TYPE_CHECKING:
    from dhis2w_client.v43.client import Dhis2Client


class DataIntegrityResult(BaseModel):
    """Result of one check — populated after the async job completes.

    Merges OpenAPI's `DataIntegrityDetails` (has `issues[]`) and
    `DataIntegritySummary` (has `count`) into one caller-friendly shape.
    Both modes populate `startTime` / `finishedTime` once the job has run;
    an unrun check returns the definition block alone.
    """

    model_config = ConfigDict(extra="allow")

    name: str
    displayName: str | None = None
    section: str | None = None
    severity: str | None = None
    code: str | None = None
    count: int | None = None
    issues: list[DataIntegrityIssue] = Field(default_factory=list)
    startTime: str | None = None
    finishedTime: str | None = None
    averageExecutionTime: int | None = None


class DataIntegrityReport(BaseModel):
    """`/api/dataIntegrity/summary` or `/details` response — keyed by check name.

    Hand-written: DHIS2 returns `{check_name: result}` — a client-side convenience
    shape not in OpenAPI. The `from_api` classmethod hides the raw-dict detail.
    """

    model_config = ConfigDict(extra="allow")

    results: dict[str, DataIntegrityResult] = Field(default_factory=dict)

    @classmethod
    def from_api(cls, raw: dict[str, Any]) -> DataIntegrityReport:
        """Validate the raw `{check_name: {...}}` dict DHIS2 returns into a typed report."""
        results = {name: DataIntegrityResult.model_validate(body) for name, body in raw.items()}
        return cls(results=results)


class IntegrityIssueRow(BaseModel):
    """One issue from a data-integrity run, tagged with its owning check's metadata.

    `iter_integrity_issues` yields these as a flat stream so callers can
    filter / transform without walking the two-level
    `{check_name: {issues: [...]}}` shape themselves.
    """

    model_config = ConfigDict(frozen=True)

    check_name: str
    check_display_name: str | None = None
    severity: str | None = None
    issue: DataIntegrityIssue


class MaintenanceAccessor:
    """`Dhis2Client.maintenance` — read paths for the data-integrity surface.

    Writes (kicking off a run, clearing cache) stay on the plugin-layer
    service in `dhis2w_core` for now — those need a `Profile` for OAuth2
    token-store keying, which the raw client doesn't know about.
    """

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client — reuses its auth + HTTP pool for every request."""
        self._client = client

    async def get_integrity_report(
        self,
        *,
        checks: Sequence[str] | None = None,
        details: bool = True,
    ) -> DataIntegrityReport:
        """Fetch the full `/api/dataIntegrity/{details|summary}` report as a typed model.

        `details=True` (the default) populates `issues[]` on each result;
        `details=False` hits the cheaper `/summary` endpoint which returns
        just counts + timing. Pass `checks` to narrow to specific check
        names (from `list_dataintegrity_checks`); omit for every check
        the last run produced.
        """
        path = "/api/dataIntegrity/details" if details else "/api/dataIntegrity/summary"
        params: dict[str, list[str]] = {"checks": list(checks)} if checks else {}
        raw = await self._client.get_raw(path, params=params or None)
        return DataIntegrityReport.from_api(raw)

    async def iter_integrity_issues(
        self,
        *,
        checks: Sequence[str] | None = None,
    ) -> AsyncIterator[IntegrityIssueRow]:
        """Stream every issue from `/api/dataIntegrity/details` one at a time.

        DHIS2's endpoint returns the whole `{check_name: {issues: [...]}}`
        structure in one response (no server-side pagination). This helper
        still buys you:

        - A flat stream — `async for row in ...` instead of nested loops.
        - Tagged rows — each yielded `IntegrityIssueRow` carries the
          owning check's name + display name + severity, so the caller
          knows the provenance without a second lookup.
        - Early break — stop iteration mid-stream without building the
          full list in memory on the Python side.

        Issues yield in the order DHIS2 returns checks, then the order
        of that check's `issues[]` list — stable across runs.
        """
        report = await self.get_integrity_report(checks=checks, details=True)
        for check_name, result in report.results.items():
            for issue in result.issues:
                yield IntegrityIssueRow(
                    check_name=check_name,
                    check_display_name=result.displayName,
                    severity=result.severity,
                    issue=issue,
                )

    async def update_category_option_combos(self) -> None:
        """Trigger DHIS2 to (re)generate the CategoryOptionCombo matrix.

        DHIS2 v42 auto-generated COCs whenever a CategoryCombo was saved,
        so callers rarely needed this. v43 changed the behavior — saving
        a CategoryCombo no longer triggers regeneration; the matrix stays
        empty until this maintenance task runs.

        `client.category_combos.wait_for_coc_generation` calls this
        helper internally before polling so the helper "just works" on
        both versions. Call it directly when you need to ensure the COC
        matrix is up to date for an existing combo (e.g. after appending
        a category via `add_category`).

        The endpoint is synchronous — DHIS2 walks every persisted combo,
        adds missing COCs, removes orphaned ones, and returns when done.
        """
        await self._client.post_raw("/api/maintenance/categoryOptionComboUpdate", {})


__all__ = [
    "DataIntegrityCheck",
    "DataIntegrityIssue",
    "DataIntegrityReport",
    "DataIntegrityResult",
    "IntegrityIssueRow",
    "JobType",
    "MaintenanceAccessor",
    "Notification",
    "NotificationDataType",
    "NotificationLevel",
]
