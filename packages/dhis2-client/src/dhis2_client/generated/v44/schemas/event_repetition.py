"""Generated EventRepetition model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import Attribute


class EventRepetition(BaseModel):
    """Generated model for DHIS2 `EventRepetition`.

    DHIS2 Event Repetition - DHIS2 resource (generated from /api/schemas at DHIS2 v44).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    dimension: str | None = None
    indexes: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    parent: Attribute | None = None
    program: str | None = None
    programStage: str | None = None
