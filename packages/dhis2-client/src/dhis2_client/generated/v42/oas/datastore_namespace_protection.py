"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ProtectionType


class DatastoreNamespaceProtection(_BaseModel):
    """OpenAPI schema `DatastoreNamespaceProtection`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    namespace: str
    readAuthorities: list[str]
    reads: ProtectionType
    writeAuthorities: list[str]
    writes: ProtectionType
