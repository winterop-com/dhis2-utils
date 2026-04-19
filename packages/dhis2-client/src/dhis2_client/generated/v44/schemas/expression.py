"""Generated Expression model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import MissingValueStrategy


class Expression(BaseModel):
    """Generated model for DHIS2 `Expression`.

    DHIS2 Expression - DHIS2 resource (generated from /api/schemas at DHIS2 v44).




    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = None

    displayDescription: str | None = None

    expression: str | None = None

    missingValueStrategy: MissingValueStrategy | None = None

    slidingWindow: bool | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
