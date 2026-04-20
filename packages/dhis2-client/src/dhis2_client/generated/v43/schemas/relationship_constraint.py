"""Generated RelationshipConstraint model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import RelationshipEntity


class RelationshipConstraint(BaseModel):
    """Generated model for DHIS2 `RelationshipConstraint`.

    DHIS2 Relationship Constraint - DHIS2 resource (generated from /api/schemas at DHIS2 v43).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    program: Reference | None = Field(default=None, description="Reference to Program.")
    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")
    relationshipEntity: RelationshipEntity | None = None
    trackedEntityType: Reference | None = Field(default=None, description="Reference to TrackedEntityType.")
    trackerDataView: Any | None = Field(default=None, description="Reference to TrackerDataView. Length/value max=255.")
