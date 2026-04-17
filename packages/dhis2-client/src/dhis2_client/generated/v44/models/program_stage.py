"""Generated ProgramStage model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ProgramStage(BaseModel):
    """DHIS2 ProgramStage resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    allowGenerateNextVisit: bool | None = None

    attributeValues: Any | None = None

    autoGenerateEvent: bool | None = None

    blockEntryForm: bool | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataEntryForm: Reference | None = None

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

    favorites: list[Any] | None = None

    featureType: str | None = None

    formName: str | None = None

    formType: str | None = None

    generatedByEnrollmentDate: bool | None = None

    hideDueDate: bool | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    minDaysFromStart: int | None = None

    name: str | None = None

    nextScheduleDate: Reference | None = None

    notificationTemplates: list[Any] | None = None

    openAfterEnrollment: bool | None = None

    periodType: str | None = None

    preGenerateUID: bool | None = None

    program: Reference | None = None

    programStageDataElements: list[Any] | None = None

    programStageLabel: str | None = None

    programStageSections: list[Any] | None = None

    referral: bool | None = None

    remindCompleted: bool | None = None

    repeatable: bool | None = None

    reportDateToUse: str | None = None

    sharing: Any | None = None

    shortName: str | None = None

    sortOrder: int | None = None

    standardInterval: int | None = None

    style: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    validationStrategy: str | None = None
