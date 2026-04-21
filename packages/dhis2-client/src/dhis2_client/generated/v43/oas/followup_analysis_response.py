"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .followup_analysis_metadata import FollowupAnalysisMetadata
    from .followup_value import FollowupValue


class FollowupAnalysisResponse(_BaseModel):
    """OpenAPI schema `FollowupAnalysisResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    followupValues: list[FollowupValue] | None = None
    metadata: FollowupAnalysisMetadata | None = None
