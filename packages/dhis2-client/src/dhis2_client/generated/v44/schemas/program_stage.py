"""Generated ProgramStage model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import FeatureType, FormType, PeriodType, ValidationStrategy


class ProgramStage(BaseModel):
    """Generated model for DHIS2 `ProgramStage`.

    DHIS2 Program Stage - persisted metadata (generated from /api/schemas at DHIS2 v44).


    API endpoint: /dev/api/programStages.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    allowGenerateNextVisit: bool | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    autoGenerateEvent: bool | None = None

    blockEntryForm: bool | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataEntryForm: Reference | None = Field(
        default=None, description="Reference to DataEntryForm. Read-only (inverse side)."
    )

    description: str | None = None

    displayDescription: str | None = None

    displayDueDateLabel: str | None = None

    displayEventLabel: str | None = None

    displayEventsLabel: str | None = None

    displayExecutionDateLabel: str | None = None

    displayFormName: str | None = None

    displayGenerateEventBox: bool | None = None

    displayName: str | None = None

    displayProgramStageLabel: str | None = None

    displayShortName: str | None = None

    dueDateLabel: str | None = None

    enableUserAssignment: bool | None = None

    eventLabel: str | None = None

    eventsLabel: str | None = None

    executionDateLabel: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    featureType: FeatureType | None = None

    formName: str | None = None

    formType: FormType | None = None

    generatedByEnrollmentDate: bool | None = None

    hideDueDate: bool | None = None

    href: str | None = None

    id: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    minDaysFromStart: int | None = None

    name: str | None = None

    nextScheduleDate: Reference | None = Field(
        default=None, description="Reference to DataElement. Read-only (inverse side)."
    )

    notificationTemplates: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    openAfterEnrollment: bool | None = None

    periodType: PeriodType | None = Field(
        default=None, description="Reference to PeriodType. Read-only (inverse side)."
    )

    preGenerateUID: bool | None = None

    program: Reference | None = Field(default=None, description="Reference to Program. Read-only (inverse side).")

    programStageDataElements: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    programStageLabel: str | None = None

    programStageSections: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    referral: bool | None = None

    remindCompleted: bool | None = None

    repeatable: bool | None = None

    reportDateToUse: str | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = None

    sortOrder: int | None = None

    standardInterval: int | None = None

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Read-only (inverse side).")

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    validationStrategy: ValidationStrategy | None = None
