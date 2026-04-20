"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DeduplicationStatus


class PotentialDuplicate(_BaseModel):
    """OpenAPI schema `PotentialDuplicate`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    createdByUserName: str | None = None
    duplicate: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedByUserName: str | None = None
    original: str | None = None
    status: DeduplicationStatus | None = None
