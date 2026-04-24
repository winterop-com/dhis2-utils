"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DataApprovalPermissions(_BaseModel):
    """OpenAPI schema `DataApprovalPermissions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    acceptedAt: datetime | None = None
    acceptedBy: str | None = None
    approvedAt: datetime | None = None
    approvedBy: str | None = None
    mayAccept: bool | None = None
    mayApprove: bool | None = None
    mayReadData: bool | None = None
    mayUnaccept: bool | None = None
    mayUnapprove: bool | None = None
    state: str | None = None
