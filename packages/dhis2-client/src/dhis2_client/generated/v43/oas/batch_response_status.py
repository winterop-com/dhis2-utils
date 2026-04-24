"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .outbound_message_response_summary import OutboundMessageResponseSummary


class BatchResponseStatus(_BaseModel):
    """OpenAPI schema `BatchResponseStatus`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    summaries: list[OutboundMessageResponseSummary] | None = None
