"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .user_details import UserDetails


class MetadataExportParamsObjectExportWithDependencies(_BaseModel):
    """A UID reference to a any type of object  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MetadataExportParams(_BaseModel):
    """OpenAPI schema `MetadataExportParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    classes: list[str] | None = None
    currentUserDetails: UserDetails | None = None
    defaultFields: list[str] | None = None
    defaultFilter: list[str] | None = None
    defaultOrder: list[str] | None = None
    defaults: str | None = None
    download: bool | None = None
    exportWithDependencies: bool | None = None
    inclusionStrategy: str | None = None
    objectExportWithDependencies: MetadataExportParamsObjectExportWithDependencies | None = _Field(
        default=None, description="A UID reference to a any type of object  "
    )
    skipSharing: bool | None = None
