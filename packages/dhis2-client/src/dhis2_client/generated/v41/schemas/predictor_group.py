"""Generated PredictorGroup model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class PredictorGroup(BaseModel):
    """DHIS2 Predictor Group - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/predictorGroups.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    description: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    displayName: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    predictors: list[Any] | None = Field(default=None, description="Collection of Predictor.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
