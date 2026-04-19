"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ImportReportMode, ImportStrategy, MergeMode, NotificationLevel


class ImportOptions(_BaseModel):
    """OpenAPI schema `ImportOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    async_: bool | None = _Field(default=None, alias="async")
    categoryIdScheme: str | None = None
    categoryOptionComboIdScheme: str | None = None
    categoryOptionIdScheme: str | None = None
    dataElementIdScheme: str | None = None
    dataSet: str | None = None
    dataSetIdScheme: str | None = None
    datasetAllowsPeriods: bool | None = None
    dryRun: bool | None = None
    filename: str | None = None
    firstRowIsHeader: bool | None = None
    force: bool | None = None
    idScheme: str | None = None
    ignoreEmptyCollection: bool | None = None
    importStrategy: ImportStrategy
    mergeDataValues: bool | None = None
    mergeMode: MergeMode
    notificationLevel: NotificationLevel
    orgUnitIdScheme: str | None = None
    preheatCache: bool | None = None
    programIdScheme: str | None = None
    programStageIdScheme: str | None = None
    reportMode: ImportReportMode
    requireAttributeOptionCombo: bool | None = None
    requireCategoryOptionCombo: bool | None = None
    sharing: bool | None = None
    skipAudit: bool | None = None
    skipCache: bool | None = None
    skipExistingCheck: bool | None = None
    skipLastUpdated: bool | None = None
    skipNotifications: bool | None = None
    skipPatternValidation: bool | None = None
    strictAttributeOptionCombos: bool | None = None
    strictCategoryOptionCombos: bool | None = None
    strictDataElements: bool | None = None
    strictDataSetApproval: bool | None = None
    strictDataSetInputPeriods: bool | None = None
    strictDataSetLocking: bool | None = None
    strictOrganisationUnits: bool | None = None
    strictPeriods: bool | None = None
    trackedEntityAttributeIdScheme: str | None = None
