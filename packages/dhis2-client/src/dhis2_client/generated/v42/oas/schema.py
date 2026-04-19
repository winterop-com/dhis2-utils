"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .authority import Authority
    from .property import Property


class Schema(_BaseModel):
    """OpenAPI schema `Schema`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    apiEndpoint: str | None = None
    authorities: list[Authority] | None = None
    collectionName: str | None = None
    dataReadShareable: bool | None = None
    dataShareable: bool | None = None
    dataWriteShareable: bool | None = None
    defaultPrivate: bool | None = None
    displayName: str | None = None
    embeddedObject: bool | None = None
    favoritable: bool | None = None
    href: str | None = None
    identifiableObject: bool | None = None
    implicitPrivateAuthority: bool | None = None
    klass: str | None = None
    metadata: bool | None = None
    name: str | None = None
    nameableObject: bool | None = None
    namespace: str | None = None
    order: int
    persisted: bool | None = None
    plural: str | None = None
    properties: list[Property] | None = None
    references: list[str] | None = None
    relativeApiEndpoint: str | None = None
    secondaryMetadata: bool | None = None
    shareable: bool | None = None
    singular: str | None = None
    subscribable: bool | None = None
    subscribableObject: bool | None = None
    translatable: bool | None = None
