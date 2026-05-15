"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class OutboundMessageResponseSummary(_BaseModel):
    """OpenAPI schema `OutboundMessageResponseSummary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    batchType: Literal["SMS", "EMAIL", "HTTP"] | None = None
    errorMessage: str | None = None
    failed: int | None = None
    pending: int | None = None
    responseMessage: str | None = None
    sent: int | None = None
    status: Literal["COMPLETED", "FAILED", "PENDING", "ABORTED"] | None = None
    total: int | None = None
