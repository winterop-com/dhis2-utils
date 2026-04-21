"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class FollowupAnalysisMetadata(_BaseModel):
    """OpenAPI schema `FollowupAnalysisMetadata`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    coc: list[str] | None = None
    de: list[str] | None = None
    endDate: datetime | None = None
    maxResults: int | None = None
    ou: list[str] | None = None
    startDate: datetime | None = None
