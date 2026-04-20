"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class LeaderNodeInfo(_BaseModel):
    """OpenAPI schema `LeaderNodeInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    currentNodeId: str | None = None
    currentNodeUuid: str | None = None
    leader: bool | None = None
    leaderNodeId: str | None = None
    leaderNodeUuid: str | None = None
