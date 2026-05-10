"""Typed models for DHIS2 v41 tracker instance data.

Thin shim over the OpenAPI-derived models under `generated/v41/oas/`. Re-exports
the wire-shape classes (`TrackerTrackedEntity`, `TrackerEnrollment`,
`TrackerEvent`, `TrackerRelationship`, `TrackerRelationshipItem`,
`TrackerDataValue`, `TrackerAttribute`, `TrackerNote`) and defines the
client-side `TrackerBundle` wrapper used for `POST /api/tracker` (not in
OpenAPI — it's the wire envelope DHIS2 accepts for bulk writes).

Unlike v42 + v43, v41 doesn't expose `EnrollmentStatus` / `EventStatus` as
typed enums — the OAS models them as plain `str` fields. Callers that need
constrained values should validate against the documented set themselves
(`ACTIVE` / `COMPLETED` / `CANCELLED` for enrollments;
`ACTIVE` / `COMPLETED` / `VISITED` / `SCHEDULE` / `OVERDUE` / `SKIPPED`
for events).

Tracker shapes drift across DHIS2 majors; keeping this under
`dhis2w_client.generated.v41` means v42 + v43 can ship their own
`generated/v{N}/oas/` + `tracker.py` without touching v41 callers.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dhis2w_client.generated.v41.oas import (
    TrackerAttribute,
    TrackerDataValue,
    TrackerEnrollment,
    TrackerEvent,
    TrackerNote,
    TrackerRelationship,
    TrackerRelationshipItem,
    TrackerTrackedEntity,
)


class TrackerBundle(BaseModel):
    """Typed payload for `POST /api/tracker` — any mix of tracker objects in one atomic write.

    DHIS2 accepts nested construction (a tracked entity carrying its own
    `enrollments[]` which carry their own `events[]`) or flat construction
    (all four arrays populated independently). Callers pick whichever fits
    their data shape; DHIS2 collapses both forms server-side.

    Produce the wire payload with
    `bundle.model_dump(by_alias=True, exclude_none=True, mode="json")`.
    Bundle fields are typed lists of the OpenAPI-derived tracker models, so
    construction-time validation catches obvious shape errors.

    Not in the OpenAPI spec — `POST /api/tracker` is documented but the
    request body shape is described only in prose. This class is a
    hand-written mirror of that shape.
    """

    model_config = ConfigDict(extra="allow")

    trackedEntities: list[TrackerTrackedEntity] = Field(default_factory=list)
    enrollments: list[TrackerEnrollment] = Field(default_factory=list)
    events: list[TrackerEvent] = Field(default_factory=list)
    relationships: list[TrackerRelationship] = Field(default_factory=list)


__all__ = [
    "TrackerAttribute",
    "TrackerBundle",
    "TrackerDataValue",
    "TrackerEnrollment",
    "TrackerEvent",
    "TrackerNote",
    "TrackerRelationship",
    "TrackerRelationshipItem",
    "TrackerTrackedEntity",
]
