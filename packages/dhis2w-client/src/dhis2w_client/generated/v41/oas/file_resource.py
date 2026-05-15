"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class FileResourceCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class FileResourceLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class FileResourceUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


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
    createdBy: FileResourceCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    domain: (
        Literal[
            "DATA_VALUE",
            "PUSH_ANALYSIS",
            "DOCUMENT",
            "MESSAGE_ATTACHMENT",
            "USER_AVATAR",
            "ORG_UNIT",
            "ICON",
            "JOB_DATA",
        ]
        | None
    ) = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    hasMultipleStorageFiles: bool | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: FileResourceLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    sharing: Sharing | None = None
    storageStatus: Literal["NONE", "PENDING", "STORED"] | None = None
    translations: list[Translation] | None = None
    user: FileResourceUser | None = _Field(default=None, description="A UID reference to a User  ")
