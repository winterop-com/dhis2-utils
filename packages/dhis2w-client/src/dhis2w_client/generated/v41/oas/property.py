"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .gist_preferences import GistPreferences


class Property(_BaseModel):
    """OpenAPI schema `Property`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    analyticalObject: bool | None = None
    apiEndpoint: str | None = None
    attribute: bool | None = None
    cascade: str | None = None
    collection: bool | None = None
    collectionName: str | None = None
    collectionWrapping: bool | None = None
    constants: list[str] | None = None
    defaultValue: dict[str, Any] | None = _Field(default=None, description="The actual type is unknown.  ")
    description: str | None = None
    embeddedObject: bool | None = None
    fieldName: str | None = None
    gistPreferences: GistPreferences | None = None
    href: str | None = None
    i18nTranslationKey: str | None = None
    identifiableObject: bool | None = None
    inverseRole: str | None = None
    itemKlass: str | None = None
    itemPropertyType: str | None = None
    klass: str | None = None
    length: int | None = None
    manyToMany: bool | None = None
    manyToOne: bool | None = None
    max: float | None = None
    min: float | None = None
    name: str | None = None
    nameableObject: bool | None = None
    namespace: str | None = None
    oneToMany: bool | None = None
    oneToOne: bool | None = None
    ordered: bool | None = None
    owner: bool | None = None
    owningRole: str | None = None
    persisted: bool | None = None
    propertyTransformer: bool | None = None
    propertyType: str | None = None
    readable: bool | None = None
    relativeApiEndpoint: str | None = None
    required: bool | None = None
    simple: bool | None = None
    translatable: bool | None = None
    translationKey: str | None = None
    unique: bool | None = None
    writable: bool | None = None
