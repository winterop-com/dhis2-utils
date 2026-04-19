"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AuditOperationType


class DataValueAuditDto(_BaseModel):
    """OpenAPI schema `DataValueAuditDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: str | None = None
    auditType: AuditOperationType
    categoryOptionCombo: str | None = None
    created: datetime | None = None
    dataElement: str | None = None
    modifiedBy: str | None = None
    orgUnit: str | None = None
    period: str | None = None
    value: str | None = None
