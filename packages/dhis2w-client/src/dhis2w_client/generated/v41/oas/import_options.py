"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


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
    eventIdScheme: str | None = None
    filename: str | None = None
    firstRowIsHeader: bool | None = None
    force: bool | None = None
    idScheme: str | None = None
    ignoreEmptyCollection: bool | None = None
    importStrategy: (
        Literal[
            "CREATE", "UPDATE", "CREATE_AND_UPDATE", "DELETE", "SYNC", "NEW_AND_UPDATES", "NEW", "UPDATES", "DELETES"
        ]
        | None
    ) = None
    mergeDataValues: bool | None = None
    mergeMode: Literal["MERGE_ALWAYS", "MERGE_IF_NOT_NULL", "MERGE", "REPLACE", "NONE"] | None = None
    notificationLevel: Literal["OFF", "DEBUG", "LOOP", "INFO", "WARN", "ERROR"] | None = None
    orgUnitIdScheme: str | None = None
    preheatCache: bool | None = None
    programIdScheme: str | None = None
    programStageIdScheme: str | None = None
    reportMode: Literal["FULL", "ERRORS", "ERRORS_NOT_OWNER", "DEBUG"] | None = None
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
    trackedEntityIdScheme: str | None = None
