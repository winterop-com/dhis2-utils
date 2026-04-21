"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import MetadataProposalStatus, MetadataProposalTarget, MetadataProposalType

if TYPE_CHECKING:
    from .user_dto import UserDto


class MetadataProposal(_BaseModel):
    """OpenAPI schema `MetadataProposal`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    change: Any | None = None
    comment: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    finalised: datetime | None = None
    finalisedBy: UserDto | None = None
    id: str | None = None
    reason: str | None = None
    status: MetadataProposalStatus | None = None
    target: MetadataProposalTarget | None = None
    targetId: str | None = None
    type: MetadataProposalType | None = None
