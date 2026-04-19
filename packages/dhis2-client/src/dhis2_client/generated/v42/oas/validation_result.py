"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject


class ValidationResult(_BaseModel):
    """OpenAPI schema `ValidationResult`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: BaseIdentifiableObject | None = None
    created: datetime | None = None
    dayInPeriod: int | None = None
    id: int | None = None
    leftsideValue: float | None = None
    notificationSent: bool | None = None
    organisationUnit: BaseIdentifiableObject | None = None
    period: BaseIdentifiableObject | None = None
    rightsideValue: float | None = None
    validationRule: BaseIdentifiableObject | None = None
