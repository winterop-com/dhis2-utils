"""Generated EventRepetition model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import Attribute


class EventRepetition(BaseModel):
    """Generated model for DHIS2 `EventRepetition`.

    DHIS2 Event Repetition - DHIS2 resource (generated from /api/schemas at DHIS2 v42).



    Transient — not stored in the DHIS2 database (computed / projection).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    dimension: str | None = Field(default=None, description="Length/value max=2147483647.")

    indexes: list[Any] | None = Field(default=None, description="Collection of Integer. Read-only (inverse side).")

    parent: Attribute | None = None

    program: str | None = Field(default=None, description="Length/value max=2147483647.")

    programStage: str | None = Field(default=None, description="Length/value max=2147483647.")
