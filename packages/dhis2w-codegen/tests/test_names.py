"""Unit tests for identifier sanitization helpers."""

from __future__ import annotations

from dhis2w_codegen.names import to_class_name, to_module_name, to_snake_case


def test_snake_case_basic() -> None:
    assert to_snake_case("dataElement") == "data_element"
    assert to_snake_case("OrganisationUnit") == "organisation_unit"
    assert to_snake_case("URL") == "u_r_l"


def test_module_name_avoids_keywords() -> None:
    assert to_module_name("class") == "class_"
    assert to_module_name("return") == "return_"


def test_module_name_sanitizes_non_identifiers() -> None:
    assert to_module_name("weird-name") == "weird_name"


def test_class_name_from_snake() -> None:
    assert to_class_name("data_element") == "DataElement"
    assert to_class_name("organisation-unit") == "OrganisationUnit"
    assert to_class_name("dataElement") == "DataElement"
