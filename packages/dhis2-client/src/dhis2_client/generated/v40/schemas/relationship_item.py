"""Generated RelationshipItem model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class RelationshipItem(BaseModel):
    """Generated model for DHIS2 `RelationshipItem`.

    DHIS2 Relationship Item - DHIS2 resource (generated from /api/schemas at DHIS2 v40).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    programInstance: Reference | None = Field(default=None, description="Reference to ProgramInstance.")
    programStageInstance: Reference | None = Field(default=None, description="Reference to ProgramStageInstance.")
    relationship: Reference | None = Field(default=None, description="Reference to Relationship.")
    trackedEntityInstance: Reference | None = Field(default=None, description="Reference to TrackedEntityInstance.")
