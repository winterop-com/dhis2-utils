"""Generated DataSet model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AggregationType, DimensionItemType, FormType, PeriodType
from .attribute_value import AttributeValue
from .data_input_period import DataInputPeriod
from .data_set_element import DataSetElement


class DataSet(BaseModel):
    """Generated model for DHIS2 `DataSet`.

    DHIS2 Data Set - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/dataSets.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )
    categoryCombo: Reference | None = Field(default=None, description="Reference to CategoryCombo.")
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    compulsoryDataElementOperands: list[Any] | None = Field(
        default=None, description="Collection of DataElementOperand."
    )
    compulsoryFieldsCompleteOnly: bool | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    dataElementDecoration: bool | None = None
    dataEntryForm: Reference | None = Field(default=None, description="Reference to DataEntryForm.")
    dataInputPeriods: list[DataInputPeriod] | None = Field(default=None, description="Collection of DataInputPeriod.")
    dataSetElements: list[DataSetElement] | None = Field(default=None, description="Collection of DataSetElement.")
    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    dimensionItem: str | None = Field(default=None, description="Read-only.")
    dimensionItemType: DimensionItemType | None = None
    displayDescription: str | None = Field(default=None, description="Read-only.")
    displayFormName: str | None = Field(default=None, description="Read-only.")
    displayName: str | None = Field(default=None, description="Read-only.")
    displayShortName: str | None = Field(default=None, description="Read-only.")
    expiryDays: int | None = Field(default=None, description="Length/value max=2147483647.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    fieldCombinationRequired: bool | None = None
    formName: str | None = Field(default=None, description="Length/value max=2147483647.")
    formType: FormType | None = Field(default=None, description="Read-only.")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    indicators: list[Any] | None = Field(default=None, description="Collection of Indicator.")
    interpretations: list[Any] | None = Field(
        default=None, description="Collection of Interpretation. Read-only (inverse side)."
    )
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")
    legendSets: list[Any] | None = Field(default=None, description="Collection of LegendSet.")
    mobile: bool | None = None
    name: str | None = Field(default=None, description="Length/value min=1, max=230.")
    noValueRequiresComment: bool | None = None
    notificationRecipients: Reference | None = Field(default=None, description="Reference to UserGroup.")
    notifyCompletingUser: bool | None = None
    openFuturePeriods: int | None = Field(default=None, description="Length/value max=2147483647.")
    openPeriodsAfterCoEndDate: int | None = Field(default=None, description="Length/value max=2147483647.")
    organisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")
    periodType: PeriodType | None = Field(default=None, description="Reference to PeriodType. Length/value max=255.")
    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")
    renderAsTabs: bool | None = None
    renderHorizontally: bool | None = None
    sections: list[Any] | None = Field(default=None, description="Collection of Section. Read-only (inverse side).")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    shortName: str | None = Field(default=None, description="Unique. Length/value min=1, max=50.")
    skipOffline: bool | None = None
    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")
    timelyDays: float | None = None
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    validCompleteOnly: bool | None = None
    version: int | None = Field(default=None, description="Length/value max=2147483647.")
    workflow: Reference | None = Field(default=None, description="Reference to DataApprovalWorkflow.")
