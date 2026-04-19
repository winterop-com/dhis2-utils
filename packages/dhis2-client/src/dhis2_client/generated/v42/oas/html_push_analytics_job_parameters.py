"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ViewMode


class HtmlPushAnalyticsJobParameters(_BaseModel):
    """OpenAPI schema `HtmlPushAnalyticsJobParameters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dashboard: str
    mode: ViewMode
    receivers: str
