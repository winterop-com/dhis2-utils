"""Unit tests for the DataValueSet + analytics Grid read models."""

from __future__ import annotations

from dhis2w_client import (
    AnalyticsMetaData,
    DataValue,
    DataValueSet,
    Grid,
    GridHeader,
)


def test_data_value_set_parses_dhis2_get_envelope() -> None:
    envelope = DataValueSet.model_validate(
        {
            "dataSet": "NORMonthDS1",
            "completeDate": None,
            "period": "202501",
            "orgUnit": "NOROsloProv",
            "dataValues": [
                {
                    "dataElement": "DEliveBirth",
                    "period": "202501",
                    "orgUnit": "NOROsloProv",
                    "categoryOptionCombo": "HllvX50cXC0",
                    "attributeOptionCombo": "HllvX50cXC0",
                    "value": "90",
                    "storedBy": "admin",
                    "created": "2026-04-18T09:47:53.000+0000",
                    "lastUpdated": "2026-04-18T09:47:53.000+0000",
                    "comment": None,
                    "followup": False,
                }
            ],
        }
    )
    assert envelope.dataSet == "NORMonthDS1"
    assert envelope.period == "202501"
    assert envelope.dataValues is not None
    assert len(envelope.dataValues) == 1
    dv = envelope.dataValues[0]
    assert isinstance(dv, DataValue)
    assert dv.dataElement == "DEliveBirth"
    assert dv.value == "90"
    assert dv.followup is False


def test_data_value_set_extra_fields_preserved() -> None:
    envelope = DataValueSet.model_validate({"dataValues": [], "futureField": "some-value"})
    assert envelope.model_dump(exclude_none=True)["futureField"] == "some-value"


def test_grid_parses_standard_analytics_envelope() -> None:
    """`Grid` accepts the full `/api/analytics` response including headers + rows + metaData."""
    grid = Grid.model_validate(
        {
            "headers": [
                {
                    "name": "dx",
                    "column": "Data",
                    "valueType": "TEXT",
                    "type": "java.lang.String",
                    "hidden": False,
                    "meta": True,
                },
                {
                    "name": "pe",
                    "column": "Period",
                    "valueType": "TEXT",
                    "type": "java.lang.String",
                    "hidden": False,
                    "meta": True,
                },
                {
                    "name": "ou",
                    "column": "Organisation unit",
                    "valueType": "TEXT",
                    "type": "java.lang.String",
                    "hidden": False,
                    "meta": True,
                },
                {
                    "name": "value",
                    "column": "Value",
                    "valueType": "NUMBER",
                    "type": "java.lang.Double",
                    "hidden": False,
                    "meta": False,
                },
            ],
            "metaData": {
                "items": {"DEancVisit1": {"name": "ANC 1st visit"}},
                "dimensions": {"dx": ["DEancVisit1"], "pe": ["202501"], "ou": ["NORNorway01"]},
            },
            "rows": [["DEancVisit1", "202501", "NORNorway01", "142"]],
            "width": 4,
            "height": 1,
            "headerWidth": 4,
        }
    )
    assert grid.headers is not None
    assert len(grid.headers) == 4
    first_header = grid.headers[0]
    assert isinstance(first_header, GridHeader)
    assert first_header.name == "dx"
    assert first_header.meta is True
    assert grid.metaData is not None
    # `Grid.metaData` is `dict[str, Any]` on the wire; lift to typed when needed.
    typed_meta = AnalyticsMetaData.model_validate(grid.metaData)
    assert typed_meta.dimensions["dx"] == ["DEancVisit1"]
    assert grid.rows == [["DEancVisit1", "202501", "NORNorway01", "142"]]
    assert grid.width == 4


def test_grid_handles_empty_body() -> None:
    """An empty body from DHIS2 still parses cleanly as a `Grid`."""
    grid = Grid.model_validate({})
    assert grid.headers is None
    assert grid.rows is None
    assert grid.metaData is None


def test_analytics_metadata_items_are_loose_dict() -> None:
    """`items` shape varies per dimension kind — we keep it as dict[str, Any] for flexibility."""
    meta = AnalyticsMetaData.model_validate(
        {
            "items": {
                "202501": {"uid": "202501", "name": "January 2025", "code": "202501", "dimensionItemType": "PERIOD"},
                "DEancVisit1": {"uid": "DEancVisit1", "name": "ANC 1st visit", "dimensionItemType": "DATA_ELEMENT"},
            },
            "dimensions": {"pe": ["202501"], "dx": ["DEancVisit1"]},
        }
    )
    assert meta.items["202501"]["name"] == "January 2025"
    assert meta.items["DEancVisit1"]["dimensionItemType"] == "DATA_ELEMENT"
