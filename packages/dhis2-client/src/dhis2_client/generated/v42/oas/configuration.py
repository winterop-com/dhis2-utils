"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject


class Configuration(_BaseModel):
    """OpenAPI schema `Configuration`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    corsAllowlist: list[str] | None = None
    corsWhitelist: list[str] | None = None
    facilityOrgUnitGroupSet: BaseIdentifiableObject | None = None
    facilityOrgUnitLevel: BaseIdentifiableObject | None = None
    feedbackRecipients: BaseIdentifiableObject | None = None
    infrastructuralDataElements: BaseIdentifiableObject | None = None
    infrastructuralIndicators: BaseIdentifiableObject | None = None
    infrastructuralPeriodType: str | None = None
    offlineOrganisationUnitLevel: BaseIdentifiableObject | None = None
    selfRegistrationOrgUnit: BaseIdentifiableObject | None = None
    selfRegistrationRole: BaseIdentifiableObject | None = None
    systemId: str | None = None
    systemUpdateNotificationRecipients: BaseIdentifiableObject | None = None
