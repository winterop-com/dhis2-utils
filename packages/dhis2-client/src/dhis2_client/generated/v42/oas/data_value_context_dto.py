"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .data_value_audit_dto import DataValueAuditDto
    from .data_value_dto import DataValueDto


class DataValueContextDto(_BaseModel):
    """OpenAPI schema `DataValueContextDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    audits: list[DataValueAuditDto] | None = None
    history: list[DataValueDto] | None = None
