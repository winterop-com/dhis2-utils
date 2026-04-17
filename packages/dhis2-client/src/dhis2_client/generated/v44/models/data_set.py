"""Generated DataSet model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataSet(BaseModel):
    """DHIS2 DataSet resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregationType: str | None = None

    attributeValues: Any | None = None

    categoryCombo: Reference | None = None

    code: str | None = None

    compulsoryDataElementOperands: list[Any] | None = None

    compulsoryFieldsCompleteOnly: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataElementDecoration: bool | None = None

    dataEntryForm: Reference | None = None

    dataInputPeriods: list[Any] | None = None

    dataSetElements: list[Any] | None = None

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayOptions: str | None = None

    displayShortName: str | None = None

    expiryDays: float | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    fieldCombinationRequired: bool | None = None

    formName: str | None = None

    formType: str | None = None

    href: str | None = None

    indicators: list[Any] | None = None

    interpretations: list[Any] | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    legendSet: Reference | None = None

    legendSets: list[Any] | None = None

    mobile: bool | None = None

    name: str | None = None

    noValueRequiresComment: bool | None = None

    notificationRecipients: Reference | None = None

    notifyCompletingUser: bool | None = None

    openFuturePeriods: int | None = None

    openPeriodsAfterCoEndDate: int | None = None

    periodType: str | None = None

    queryMods: Any | None = None

    renderAsTabs: bool | None = None

    renderHorizontally: bool | None = None

    sections: list[Any] | None = None

    sharing: Any | None = None

    shortName: str | None = None

    skipOffline: bool | None = None

    sources: list[Any] | None = None

    style: Any | None = None

    timelyDays: float | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    validCompleteOnly: bool | None = None

    version: int | None = None

    workflow: Reference | None = None
