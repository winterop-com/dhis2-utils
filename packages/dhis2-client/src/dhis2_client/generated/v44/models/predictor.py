"""Generated Predictor model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Predictor(BaseModel):
    """DHIS2 Predictor resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    annualSampleCount: int | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    formName: str | None = None

    generator: Any | None = None

    groups: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    organisationUnitDescendants: str | None = None

    organisationUnitLevels: list[Any] | None = None

    output: Reference | None = None

    outputCombo: Reference | None = None

    periodType: str | None = None

    sampleSkipTest: Any | None = None

    sequentialSampleCount: int | None = None

    sequentialSkipCount: int | None = None

    sharing: Any | None = None

    shortName: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
