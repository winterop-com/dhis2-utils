"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import Status

if TYPE_CHECKING:
    pass


class WebMessage(_BaseModel):
    """OpenAPI schema `WebMessage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: int | None = None
    devMessage: str | None = None
    errorCode: str | None = None
    httpStatus: str | None = None
    httpStatusCode: int | None = None
    message: str | None = None
    response: dict[str, Any] | None = None
    status: Status | None = None
