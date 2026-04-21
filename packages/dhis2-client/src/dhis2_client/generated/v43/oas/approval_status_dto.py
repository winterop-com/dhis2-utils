"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import DataApprovalState

if TYPE_CHECKING:
    from .data_approval_permissions import DataApprovalPermissions


class ApprovalStatusDtoPe(_BaseModel):
    """OpenAPI schema `ApprovalStatusDtoPe`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ApprovalStatusDto(_BaseModel):
    """OpenAPI schema `ApprovalStatusDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aoc: str | None = None
    level: str | None = None
    ou: str | None = None
    ouName: str | None = None
    pe: ApprovalStatusDtoPe | None = None
    permissions: DataApprovalPermissions | None = None
    state: DataApprovalState | None = None
    wf: str | None = None
