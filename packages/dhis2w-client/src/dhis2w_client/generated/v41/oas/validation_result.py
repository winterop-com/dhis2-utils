"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class ValidationResultAttributeOptionCombo(_BaseModel):
    """A UID reference to a CategoryOptionCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationResultOrganisationUnit(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationResultValidationRule(_BaseModel):
    """A UID reference to a ValidationRule  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationResult(_BaseModel):
    """OpenAPI schema `ValidationResult`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: ValidationResultAttributeOptionCombo | None = _Field(
        default=None, description="A UID reference to a CategoryOptionCombo  "
    )
    created: datetime | None = None
    dayInPeriod: int | None = None
    id: int | None = None
    leftsideValue: float | None = None
    notificationSent: bool | None = None
    organisationUnit: ValidationResultOrganisationUnit | None = _Field(
        default=None, description="A UID reference to a OrganisationUnit  "
    )
    period: str | None = None
    rightsideValue: float | None = None
    validationRule: ValidationResultValidationRule | None = _Field(
        default=None, description="A UID reference to a ValidationRule  "
    )
