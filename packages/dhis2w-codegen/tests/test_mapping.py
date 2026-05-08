"""Unit tests for the DHIS2 property → Python type mapping."""

from __future__ import annotations

from dhis2w_codegen.mapping import python_type_for


def test_primitive_types() -> None:
    assert python_type_for({"propertyType": "TEXT"}) == "str"
    assert python_type_for({"propertyType": "BOOLEAN"}) == "bool"
    assert python_type_for({"propertyType": "INTEGER"}) == "int"
    assert python_type_for({"propertyType": "NUMBER"}) == "float"
    assert python_type_for({"propertyType": "DATE"}) == "datetime"
    assert python_type_for({"propertyType": "DATETIME"}) == "datetime"


def test_collection_wraps_inner_type() -> None:
    assert python_type_for({"propertyType": "TEXT", "collection": True}) == "list[str]"


def test_reference_with_klass_uses_class_name() -> None:
    spec = {"propertyType": "REFERENCE", "klass": "org.hisp.dhis.dataelement.DataElement"}
    assert python_type_for(spec) == "Reference"  # defaults to Reference — v1 keeps refs shallow


def test_reference_without_klass_falls_back_to_reference() -> None:
    assert python_type_for({"propertyType": "REFERENCE"}) == "Reference"


def test_complex_becomes_any() -> None:
    # COMPLEX fields vary in DHIS2 (dict, list, empty list) — Any is the honest type.
    assert python_type_for({"propertyType": "COMPLEX"}) == "Any"


def test_unknown_type_becomes_any() -> None:
    assert python_type_for({"propertyType": "SOMETHING_NEW"}) == "Any"
