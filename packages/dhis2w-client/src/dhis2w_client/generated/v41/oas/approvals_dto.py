"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .approval_dto import ApprovalDto


class ApprovalsDto(_BaseModel):
    """OpenAPI schema `ApprovalsDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    approvals: list[ApprovalDto] | None = None
    ds: list[str] | None = None
    pe: list[str] | None = None
    wf: list[str] | None = None
