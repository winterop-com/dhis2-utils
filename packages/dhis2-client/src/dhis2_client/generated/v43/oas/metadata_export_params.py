"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import Defaults

if TYPE_CHECKING:
    from .identifiable_object import IdentifiableObject
    from .user_details import UserDetails


class MetadataExportParams(_BaseModel):
    """OpenAPI schema `MetadataExportParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    classes: list[str] | None = None
    currentUserDetails: UserDetails | None = None
    defaultFields: list[str] | None = None
    defaultFilter: list[str] | None = None
    defaultOrder: list[str] | None = None
    defaults: Defaults | None = None
    download: bool | None = None
    exportWithDependencies: bool | None = None
    inclusionStrategy: str | None = None
    objectExportWithDependencies: IdentifiableObject | None = None
    skipSharing: bool | None = None
