"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .data_approval_permissions import DataApprovalPermissions


class DataApprovalStateResponse(_BaseModel):
    """OpenAPI schema `DataApprovalStateResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    createdByUsername: str | None = None
    createdDate: datetime | None = None
    dataSet: BaseIdentifiableObject | None = None
    organisationUnit: BaseIdentifiableObject | None = None
    period: BaseIdentifiableObject | None = None
    permissions: DataApprovalPermissions | None = None
    state: str | None = None
