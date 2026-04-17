"""Generated ValidationRule model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ValidationRule(BaseModel):
    """DHIS2 ValidationRule resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregateExportAttributeOptionCombo: str | None = None

    aggregateExportCategoryOptionCombo: str | None = None

    aggregationType: str | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayInstruction: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    formName: str | None = None

    groups: list[Any] | None = None

    href: str | None = None

    importance: str | None = None

    instruction: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    leftSide: Any | None = None

    legendSet: Reference | None = None

    legendSets: list[Any] | None = None

    name: str | None = None

    notificationTemplates: list[Any] | None = None

    operator: str | None = None

    organisationUnitLevels: list[Any] | None = None

    periodType: str | None = None

    queryMods: Any | None = None

    rightSide: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    skipFormValidation: bool | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
