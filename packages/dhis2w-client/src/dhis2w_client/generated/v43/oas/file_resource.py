"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import FileResourceDomain, FileResourceStorageStatus

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class FileResource(_BaseModel):
    """OpenAPI schema `FileResource`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    assigned: bool | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    contentLength: int | None = None
    contentMd5: str | None = None
    contentType: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    displayName: str | None = None
    domain: FileResourceDomain | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    hasMultipleStorageFiles: bool | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    name: str | None = None
    sharing: Sharing | None = None
    storageStatus: FileResourceStorageStatus | None = None
    translations: list[Translation] | None = None
