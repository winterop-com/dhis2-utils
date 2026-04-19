"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DashboardInfo(_BaseModel):
    """OpenAPI schema `DashboardInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    unreadInterpretations: int
    unreadMessageConversations: int
