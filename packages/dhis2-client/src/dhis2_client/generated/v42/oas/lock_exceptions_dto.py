"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .lock_exception_dto import LockExceptionDto


class LockExceptionsDto(_BaseModel):
    """OpenAPI schema `LockExceptionsDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    lockExceptions: list[LockExceptionDto] | None = None
