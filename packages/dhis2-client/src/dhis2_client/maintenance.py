"""Typed models for DHIS2 maintenance + data-integrity + task-notification APIs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Notification(BaseModel):
    """One entry in the `/api/system/tasks/{type}/{uid}` notifier feed.

    DHIS2 accumulates `Notification` rows per background job. A `completed=true`
    row with `level=INFO|WARN|ERROR` signals the job finished. The final
    message usually carries a human summary (e.g. `Analytics tables updated:
    00:00:03.795`); `ERROR` rows carry failure detail.
    """

    model_config = ConfigDict(extra="allow")

    level: str | None = None
    category: str | None = None
    message: str | None = None
    completed: bool = False
    id: str | None = None
    uid: str | None = None
    time: str | None = None


class DataIntegrityCheck(BaseModel):
    """One entry returned by `GET /api/dataIntegrity` — the definition of a check.

    Every check has a stable `name` (used as the `checks=` query-param value
    when running it), a human-readable `displayName` / `section` / `description`
    block, a `severity` tag (`INFO` / `WARNING` / `SEVERE` / `CRITICAL`), and
    metadata describing which resource type it inspects (`issuesIdType`) and
    whether it runs via SQL view (`isProgrammatic=false`) or code
    (`isProgrammatic=true`). `isSlow=true` marks checks that should be run
    off-peak.
    """

    model_config = ConfigDict(extra="allow")

    name: str
    displayName: str | None = None
    section: str | None = None
    sectionOrder: int | None = None
    severity: str | None = None
    description: str | None = None
    introduction: str | None = None
    recommendation: str | None = None
    issuesIdType: str | None = None
    isSlow: bool = False
    isProgrammatic: bool = False
    code: str | None = None


class DataIntegrityIssue(BaseModel):
    """One offending row surfaced by a data-integrity check (details mode only)."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    refs: list[str] | None = None
    comment: str | None = None


class DataIntegrityResult(BaseModel):
    """Result of one check — populated after the async job completes.

    `count` (summary mode) is the number of offending rows; `issues[]` (details
    mode) carries the rows themselves. Both modes populate `startTime` /
    `finishedTime` once the job has run; an unrun check returns the definition
    block alone.
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
    """`/api/dataIntegrity/summary` or `/details` response — keyed by check name."""

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
