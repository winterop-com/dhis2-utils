"""Pydantic models for DHIS2's WebMessageResponse + ImportReport envelopes.

These shapes are universal across DHIS2 versions (derived from
`/api/openapi.json#/components/schemas/{WebMessage,ObjectReport,ImportReport,...}`).
Every POST/PUT/DELETE/PATCH through `/api/*` returns one of them.

The top-level `WebMessageResponse` has an optional `response` field whose
subtype depends on the endpoint — we keep it as `dict[str, Any] | None` here
so the envelope itself is typed while callers who need the inner shape can
validate it against a more specific model (e.g. `ObjectReport`,
`ImportCount`, `ImportReport`).

Convenience: `WebMessageResponse.created_uid` returns the `response.uid`
field when present — closes out the BUGS.md #4f defensive lookups.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorReport(BaseModel):
    """One error from a DHIS2 import report."""

    model_config = ConfigDict(extra="allow")

    message: str | None = None
    errorCode: str | None = None
    errorKlass: str | None = None
    errorProperty: str | None = None
    errorProperties: list[Any] | None = None
    mainId: str | None = None
    mainKlass: str | None = None
    args: list[str] | None = None


class ObjectReport(BaseModel):
    """Per-object report inside DHIS2's ImportReport — one entry per created/updated/ignored object."""

    model_config = ConfigDict(extra="allow")

    uid: str | None = None
    klass: str | None = None
    displayName: str | None = None
    index: int | None = None
    errorReports: list[ErrorReport] = Field(default_factory=list)


class ImportCount(BaseModel):
    """Data-value import counts returned by `/api/dataValueSets`."""

    model_config = ConfigDict(extra="allow")

    imported: int = 0
    updated: int = 0
    ignored: int = 0
    deleted: int = 0


class Stats(BaseModel):
    """Aggregate metadata import stats — `created + updated + deleted + ignored = total`."""

    model_config = ConfigDict(extra="allow")

    created: int | None = None
    updated: int | None = None
    deleted: int | None = None
    ignored: int | None = None
    total: int | None = None


class TypeReport(BaseModel):
    """Per-resource-type report inside an ImportReport (e.g. one entry per resource class imported)."""

    model_config = ConfigDict(extra="allow")

    klass: str | None = None
    stats: Stats | None = None
    objectReports: list[ObjectReport] = Field(default_factory=list)


class ImportReport(BaseModel):
    """Full `/api/metadata` bulk-import report."""

    model_config = ConfigDict(extra="allow")

    status: str | None = None
    stats: Stats | None = None
    typeReports: list[TypeReport] = Field(default_factory=list)


class WebMessageResponse(BaseModel):
    """Top-level envelope DHIS2 wraps every write response in.

    `httpStatus` is the text form (`"OK"`, `"Created"`, `"Conflict"`, ...);
    `httpStatusCode` is the numeric code. `status` is the server's own
    `Status` enum value (`"OK"`, `"WARNING"`, `"ERROR"`). `response` is an
    endpoint-specific inner shape — commonly `ObjectReport` for CRUD,
    `ImportReport` for bulk metadata, `ImportCount` for data values,
    `TrackerJobWebMessageResponse` for tracker imports, etc.
    """

    model_config = ConfigDict(extra="allow")

    httpStatus: str | None = None
    httpStatusCode: int | None = None
    status: str | None = None
    code: int | None = None
    message: str | None = None
    devMessage: str | None = None
    errorCode: str | None = None
    response: dict[str, Any] | None = None

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

    def object_report(self) -> ObjectReport | None:
        """Validate `response` as an `ObjectReport` — useful after single-object CRUD."""
        return ObjectReport.model_validate(self.response) if self.response else None

    def import_count(self) -> ImportCount | None:
        """Validate `response` as an `ImportCount` — useful after data-value imports."""
        return ImportCount.model_validate(self.response) if self.response else None

    def import_report(self) -> ImportReport | None:
        """Validate `response` as an `ImportReport` — useful after metadata bulk imports."""
        return ImportReport.model_validate(self.response) if self.response else None


__all__ = [
    "ErrorReport",
    "ImportCount",
    "ImportReport",
    "ObjectReport",
    "Stats",
    "TypeReport",
    "WebMessageResponse",
]
