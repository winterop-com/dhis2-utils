"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ObjectValueTypeRenderingOption(_BaseModel):
    """OpenAPI schema `ObjectValueTypeRenderingOption`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    clazz: str | None = None
    hasOptionSet: bool | None = None
    renderingTypes: (
        list[
            Literal[
                "DEFAULT",
                "DROPDOWN",
                "VERTICAL_RADIOBUTTONS",
                "HORIZONTAL_RADIOBUTTONS",
                "VERTICAL_CHECKBOXES",
                "HORIZONTAL_CHECKBOXES",
                "SHARED_HEADER_RADIOBUTTONS",
                "ICONS_AS_BUTTONS",
                "SPINNER",
                "ICON",
                "TOGGLE",
                "VALUE",
                "SLIDER",
                "LINEAR_SCALE",
                "AUTOCOMPLETE",
                "QR_CODE",
                "BAR_CODE",
                "GS1_DATAMATRIX",
                "CANVAS",
            ]
        ]
        | None
    ) = None
    valueType: (
        Literal[
            "TEXT",
            "LONG_TEXT",
            "MULTI_TEXT",
            "LETTER",
            "PHONE_NUMBER",
            "EMAIL",
            "BOOLEAN",
            "TRUE_ONLY",
            "DATE",
            "DATETIME",
            "TIME",
            "NUMBER",
            "UNIT_INTERVAL",
            "PERCENTAGE",
            "INTEGER",
            "INTEGER_POSITIVE",
            "INTEGER_NEGATIVE",
            "INTEGER_ZERO_OR_POSITIVE",
            "TRACKER_ASSOCIATE",
            "USERNAME",
            "COORDINATE",
            "ORGANISATION_UNIT",
            "REFERENCE",
            "AGE",
            "URL",
            "FILE_RESOURCE",
            "IMAGE",
            "GEOJSON",
        ]
        | None
    ) = None
