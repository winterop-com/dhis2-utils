"""Typed models for DHIS2 v42 tracker instance data.

Thin shim over the OpenAPI-derived models under `generated/v42/oas/`. Re-exports
the wire-shape classes (`TrackerTrackedEntity`, `TrackerEnrollment`,
`TrackerEvent`, `TrackerRelationship`, `TrackerRelationshipItem`,
`TrackerDataValue`, `TrackerAttribute`, `TrackerNote`) plus the status enums
(`EnrollmentStatus`, `EventStatus`), and defines the client-side `TrackerBundle`
wrapper used for `POST /api/tracker` (not in OpenAPI — it's the wire envelope
DHIS2 accepts for bulk writes).

Tracker shapes drift across DHIS2 majors; keeping this under
`dhis2w_client.generated.v42` means a v43 bump can ship its own
`generated/v43/oas/` + `tracker.py` without touching v42 callers.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dhis2w_client.generated.v42.oas import (
    EnrollmentStatus,
    EventStatus,
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
    enum fields like `EventStatus.COMPLETED` validate at construction time.

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
    "EnrollmentStatus",
    "EventStatus",
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
