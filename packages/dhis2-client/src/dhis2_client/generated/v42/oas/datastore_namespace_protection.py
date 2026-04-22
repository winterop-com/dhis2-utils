"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ProtectionType


class DatastoreNamespaceProtection(_BaseModel):
    """OpenAPI schema `DatastoreNamespaceProtection`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    namespace: str | None = None
    readAuthorities: list[str] | None = None
    reads: ProtectionType | None = None
    writeAuthorities: list[str] | None = None
    writes: ProtectionType | None = None
