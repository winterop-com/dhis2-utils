"""Generated ProgramStage model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import FeatureType, FormType, PeriodType, ValidationStrategy
from .attribute_value import AttributeValue


class ProgramStage(BaseModel):
    """Generated model for DHIS2 `ProgramStage`.

    DHIS2 Program Stage - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/programStages.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    allowGenerateNextVisit: bool | None = None
    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )
    autoGenerateEvent: bool | None = None
    blockEntryForm: bool | None = None
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    dataEntryForm: Reference | None = Field(default=None, description="Reference to DataEntryForm.")
    description: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")
    displayDescription: str | None = Field(default=None, description="Read-only.")
    displayDueDateLabel: str | None = Field(default=None, description="Read-only.")
    displayEventLabel: str | None = Field(default=None, description="Read-only.")
    displayExecutionDateLabel: str | None = Field(default=None, description="Read-only.")
    displayFormName: str | None = Field(default=None, description="Read-only.")
    displayGenerateEventBox: bool | None = None
    displayName: str | None = Field(default=None, description="Read-only.")
    displayProgramStageLabel: str | None = Field(default=None, description="Read-only.")
    displayShortName: str | None = Field(default=None, description="Read-only.")
    dueDateLabel: str | None = Field(default=None, description="Length/value min=2, max=255.")
    enableUserAssignment: bool | None = None
    eventLabel: str | None = Field(default=None, description="Length/value min=2, max=255.")
    executionDateLabel: str | None = Field(default=None, description="Length/value min=2, max=255.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    featureType: FeatureType | None = None
    formName: str | None = Field(default=None, description="Length/value max=2147483647.")
    formType: FormType | None = Field(default=None, description="Read-only.")
    generatedByEnrollmentDate: bool | None = None
    hideDueDate: bool | None = None
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    minDaysFromStart: int | None = Field(default=None, description="Length/value max=2147483647.")
    name: str | None = Field(default=None, description="Length/value min=1, max=230.")
    nextScheduleDate: Reference | None = Field(default=None, description="Reference to DataElement.")
    notificationTemplates: list[Any] | None = Field(
        default=None, description="Collection of ProgramNotificationTemplate."
    )
    openAfterEnrollment: bool | None = None
    periodType: PeriodType | None = Field(default=None, description="Reference to PeriodType. Length/value max=255.")
    preGenerateUID: bool | None = None
    program: Reference | None = Field(default=None, description="Reference to Program.")
    programStageDataElements: list[Any] | None = Field(
        default=None, description="Collection of ProgramStageDataElement."
    )
    programStageLabel: str | None = Field(default=None, description="Length/value min=2, max=255.")
    programStageSections: list[Any] | None = Field(default=None, description="Collection of ProgramStageSection.")
    referral: bool | None = None
    remindCompleted: bool | None = None
    repeatable: bool | None = None
    reportDateToUse: str | None = Field(default=None, description="Length/value max=255.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    shortName: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")
    standardInterval: int | None = Field(default=None, description="Length/value max=2147483647.")
    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    validationStrategy: ValidationStrategy | None = None
