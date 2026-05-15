"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .data_approval_permissions import DataApprovalPermissions


class ApprovalStatusDto(_BaseModel):
    """OpenAPI schema `ApprovalStatusDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aoc: str | None = _Field(default=None, description="A UID for an CategoryOptionCombo object  ")
    level: str | None = None
    ou: str | None = _Field(default=None, description="A UID for an OrganisationUnit object  ")
    ouName: str | None = None
    pe: str | None = None
    permissions: DataApprovalPermissions | None = None
    state: (
        Literal[
            "UNAPPROVABLE",
            "UNAPPROVED_ABOVE",
            "UNAPPROVED_WAITING",
            "UNAPPROVED_READY",
            "APPROVED_ABOVE",
            "APPROVED_HERE",
            "ACCEPTED_HERE",
        ]
        | None
    ) = None
    wf: str | None = _Field(default=None, description="A UID for an DataApprovalWorkflow object  ")
