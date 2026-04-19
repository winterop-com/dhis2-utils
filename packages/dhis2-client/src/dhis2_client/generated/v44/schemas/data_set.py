"""Generated DataSet model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AggregationType, DimensionItemType, FormType, PeriodType


class DataSet(BaseModel):
    """Generated model for DHIS2 `DataSet`.

    DHIS2 Data Set - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/dataSets.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    aggregationType: AggregationType | None = None
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    categoryCombo: Reference | None = Field(
        default=None, description="Reference to CategoryCombo. Read-only (inverse side)."
    )
    code: str | None = None
    compulsoryDataElementOperands: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    compulsoryFieldsCompleteOnly: bool | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    dataElementDecoration: bool | None = None
    dataEntryForm: Reference | None = Field(
        default=None, description="Reference to DataEntryForm. Read-only (inverse side)."
    )
    dataInputPeriods: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    dataSetElements: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    description: str | None = None
    dimensionItem: str | None = None
    dimensionItemType: DimensionItemType | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayOptions: str | None = None
    displayShortName: str | None = None
    expiryDays: float | None = None
    favorite: bool | None = None
    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    fieldCombinationRequired: bool | None = None
    formName: str | None = None
    formType: FormType | None = None
    href: str | None = None
    id: str | None = None
    indicators: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    interpretations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")
    legendSets: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    mobile: bool | None = None
    name: str | None = None
    noValueRequiresComment: bool | None = None
    notificationRecipients: Reference | None = Field(
        default=None, description="Reference to UserGroup. Read-only (inverse side)."
    )
    notifyCompletingUser: bool | None = None
    openFuturePeriods: int | None = None
    openPeriodsAfterCoEndDate: int | None = None
    organisationUnits: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    periodType: PeriodType | None = Field(
        default=None, description="Reference to PeriodType. Read-only (inverse side)."
    )
    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")
    renderAsTabs: bool | None = None
    renderHorizontally: bool | None = None
    sections: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    shortName: str | None = None
    skipOffline: bool | None = None
    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Read-only (inverse side).")
    timelyDays: float | None = None
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    validCompleteOnly: bool | None = None
    version: int | None = None
    workflow: Reference | None = Field(
        default=None, description="Reference to DataApprovalWorkflow. Read-only (inverse side)."
    )
