"""Generated Predictor model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import OrganisationUnitDescendants


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Predictor(BaseModel):
    """DHIS2 Predictor - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/predictors.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    annualSampleCount: int | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    description: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    formName: str | None = None

    generator: Any | None = Field(default=None, description="Reference to Expression. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    name: str | None = None

    organisationUnitDescendants: OrganisationUnitDescendants | None = None

    organisationUnitLevels: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    output: Reference | None = Field(default=None, description="Reference to DataElement. Read-only (inverse side).")

    outputCombo: Reference | None = Field(
        default=None, description="Reference to CategoryOptionCombo. Read-only (inverse side)."
    )

    periodType: str | None = Field(default=None, description="Reference to PeriodType. Read-only (inverse side).")

    predictorGroups: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    sampleSkipTest: Any | None = Field(default=None, description="Reference to Expression. Read-only (inverse side).")

    sequentialSampleCount: int | None = None

    sequentialSkipCount: int | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
