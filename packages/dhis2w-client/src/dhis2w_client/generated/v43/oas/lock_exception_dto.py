"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class LockExceptionDto(_BaseModel):
    """OpenAPI schema `LockExceptionDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataSet: str | None = None
    orgUnit: str | None = None
    period: str | None = None
