"""DHIS2 WebMessageResponse + ImportReport envelopes (shim over generated/v42/oas).

The raw shapes come from `/api/openapi.json#/components/schemas/{WebMessage,
ObjectReport, ImportReport, TypeReport, Stats, ErrorReport, ImportConflict,
ImportCount}` — see `dhis2_client.generated.v42.oas`. This module re-exports
those classes under their domain names and adds the helper methods
(`created_uid`, `task_ref`, `object_report`, `import_count`, `import_report`,
`conflicts`, `rejected_indexes`) on `WebMessageResponse` that callers rely on.

Every POST/PUT/DELETE/PATCH through `/api/*` returns a `WebMessageResponse`.
Its `response` field carries an endpoint-specific payload; the helper methods
project it into the right typed shape (`ObjectReport` for CRUD, `ImportReport`
for `/api/metadata`, `ImportCount` for `/api/dataValueSets`, etc.).
"""

from __future__ import annotations

from typing import Any

from dhis2_client.generated.v42.oas import (
    ErrorReport,
    ImportConflict,
    ImportCount,
    ImportReport,
    ObjectReport,
    Stats,
    TypeReport,
    WebMessage,
)

# Conflict keeps the local name callers use for per-row rejection; OpenAPI
# names the wire schema `ImportConflict`. Alias so the public API is stable.
Conflict = ImportConflict


class WebMessageResponse(WebMessage):
    """DHIS2 write-response envelope with typed helper accessors.

    Inherits every wire field from `WebMessage` (`httpStatus`, `httpStatusCode`,
    `status`, `code`, `message`, `devMessage`, `errorCode`, `response`) and adds
    helper methods that project the endpoint-specific `response` dict into the
    right typed shape.
    """

    @property
    def created_uid(self) -> str | None:
        """Pull `response.uid` when the inner envelope is an ObjectReport.

        DHIS2's ObjectReport names the created identifier `uid` (not `id`) —
        see BUGS.md #4f. This property hides the defensive lookup.
        """
        if self.response is None:
            return None
        uid = self.response.get("uid") or self.response.get("id")
        return str(uid) if uid else None

    def task_ref(self) -> tuple[str, str] | None:
        """Return `(job_type, task_uid)` when DHIS2 returned a job-kickoff envelope.

        Every `/api/*/async` or `/api/resourceTables/analytics`-style endpoint
        returns a `JobConfigurationWebMessageResponse` with `response.jobType`
        and `response.id`. Callers that want to watch the job to completion
        feed this tuple to `maintenance.service.watch_task`.
        """
        if self.response is None:
            return None
        job_type = self.response.get("jobType")
        task_uid = self.response.get("id")
        if isinstance(job_type, str) and isinstance(task_uid, str):
            return job_type, task_uid
        return None

    def object_report(self) -> ObjectReport | None:
        """Validate `response` as an `ObjectReport` — useful after single-object CRUD."""
        return ObjectReport.model_validate(self.response) if self.response else None

    def import_count(self) -> ImportCount | None:
        """Validate `response` (or `response.importCount`) as an `ImportCount`.

        DHIS2 uses two shapes for the counts: some endpoints inline them at
        `response.imported` / `response.updated` / ...; others nest them under
        `response.importCount = {...}`. Both reach the same parsed model.
        """
        if not self.response:
            return None
        nested = self.response.get("importCount")
        if isinstance(nested, dict):
            return ImportCount.model_validate(nested)
        return ImportCount.model_validate(self.response)

    def import_report(self) -> ImportReport | None:
        """Validate `response` as an `ImportReport` — useful after metadata bulk imports."""
        return ImportReport.model_validate(self.response) if self.response else None

    def conflicts(self) -> list[Conflict]:
        """Pull `response.conflicts[]` — per-row rejections from a data-value or tracker import."""
        if not self.response:
            return []
        raw = self.response.get("conflicts") or []
        if not isinstance(raw, list):
            return []
        return [Conflict.model_validate(item) for item in raw]

    def rejected_indexes(self) -> list[int]:
        """Pull `response.rejectedIndexes[]` — payload-array indexes DHIS2 refused to import."""
        if not self.response:
            return []
        raw = self.response.get("rejectedIndexes") or []
        if not isinstance(raw, list):
            return []
        return [int(idx) for idx in raw if isinstance(idx, int)]


# Re-bound types for the static checker. `Any` kept so callers importing it
# from here (historical pattern) still work.
_ = Any


__all__ = [
    "Conflict",
    "ErrorReport",
    "ImportCount",
    "ImportReport",
    "ObjectReport",
    "Stats",
    "TypeReport",
    "WebMessageResponse",
]
