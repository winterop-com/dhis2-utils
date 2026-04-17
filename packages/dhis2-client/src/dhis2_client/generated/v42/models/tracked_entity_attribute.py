"""Generated TrackedEntityAttribute model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class TrackedEntityAttribute(BaseModel):
    """DHIS2 TrackedEntityAttribute resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregationType: str | None = None

    attributeValues: Any | None = None

    code: str | None = None

    confidential: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayInListNoProgram: bool | None = None

    displayName: str | None = None

    displayOnVisitSchedule: bool | None = None

    displayShortName: str | None = None

    expression: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    fieldMask: str | None = None

    formName: str | None = None

    generated: bool | None = None

    href: str | None = None

    inherit: bool | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    legendSet: Reference | None = None

    legendSets: list[Any] | None = None

    name: str | None = None

    optionSet: Reference | None = None

    optionSetValue: bool | None = None

    orgunitScope: bool | None = None

    pattern: str | None = None

    queryMods: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    skipSynchronization: bool | None = None

    sortOrderInListNoProgram: int | None = None

    sortOrderInVisitSchedule: int | None = None

    style: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    unique: bool | None = None

    user: Reference | None = None

    valueType: str | None = None
