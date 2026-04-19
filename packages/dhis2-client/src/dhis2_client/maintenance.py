"""Typed models for DHIS2 maintenance + data-integrity + task-notification APIs.

`DataIntegrityCheck` and `DataIntegrityIssue` come from
`dhis2_client.generated.v42.oas`. `DataIntegrityResult` and
`DataIntegrityReport` stay hand-written — OpenAPI splits the result into
separate `DataIntegrityDetails` / `DataIntegritySummary` shapes, but this
module's callers want the merged view + the client-side `{check_name: result}`
map. `Notification` stays hand-written while OpenAPI's typed
`category` / `dataType` / `level` enums are integrated cautiously.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dhis2_client.generated.v42.oas import DataIntegrityCheck, DataIntegrityIssue


class Notification(BaseModel):
    """One entry in the `/api/system/tasks/{type}/{uid}` notifier feed.

    DHIS2 accumulates `Notification` rows per background job. A `completed=true`
    row with `level=INFO|WARN|ERROR` signals the job finished. The final
    message usually carries a human summary (e.g. `Analytics tables updated:
    00:00:03.795`); `ERROR` rows carry failure detail.

    Hand-written: OpenAPI's `Notification` schema ships typed `category`,
    `dataType`, and `level` enums, but integrating them requires threading
    new enum types through every caller. Leave as permissive strings until
    a follow-up wires the enums in.
    """

    model_config = ConfigDict(extra="allow")

    level: str | None = None
    category: str | None = None
    message: str | None = None
    completed: bool = False
    id: str | None = None
    uid: str | None = None
    time: str | None = None


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


__all__ = [
    "DataIntegrityCheck",
    "DataIntegrityIssue",
    "DataIntegrityReport",
    "DataIntegrityResult",
    "Notification",
]
