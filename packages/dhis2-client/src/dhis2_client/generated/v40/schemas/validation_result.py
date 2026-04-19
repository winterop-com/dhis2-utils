"""Generated ValidationResult model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class ValidationResult(BaseModel):
    """Generated model for DHIS2 `ValidationResult`.

    DHIS2 Validation Result - DHIS2 resource (generated from /api/schemas at DHIS2 v40).


    API endpoint: /api/validationResults.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attributeOptionCombo: Reference | None = Field(
        default=None, description="Reference to CategoryOptionCombo. Read-only (inverse side)."
    )

    created: datetime | None = None

    dayInPeriod: int | None = Field(default=None, description="Length/value max=2147483647.")

    id: str | None = Field(default=None, description="Length/value max=2147483647.")

    leftsideValue: float | None = None

    notificationSent: bool | None = None

    organisationUnit: Reference | None = Field(
        default=None, description="Reference to OrganisationUnit. Read-only (inverse side)."
    )

    period: Reference | None = Field(default=None, description="Reference to Period. Read-only (inverse side).")

    rightsideValue: float | None = None

    validationRule: Reference | None = Field(
        default=None, description="Reference to ValidationRule. Read-only (inverse side)."
    )
