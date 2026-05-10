"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class DataValueAuditDto(_BaseModel):
    """OpenAPI schema `DataValueAuditDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: str | None = _Field(default=None, description="A UID for an CategoryOptionCombo object  ")
    auditType: str | None = None
    categoryOptionCombo: str | None = _Field(default=None, description="A UID for an CategoryOptionCombo object  ")
    created: datetime | None = None
    dataElement: str | None = _Field(default=None, description="A UID for an DataElement object  ")
    modifiedBy: str | None = None
    orgUnit: str | None = _Field(default=None, description="A UID for an OrganisationUnit object  ")
    period: str | None = None
    value: str | None = None
