"""v41 envelopes target `generated.v41.oas` + carry local ImportConflict/ImportCount stubs."""

from __future__ import annotations

import httpx
import respx
from dhis2w_client import BasicAuth, Dhis2Client
from dhis2w_client.v41.envelopes import (
    ImportConflict as V41ImportConflict,
)
from dhis2w_client.v41.envelopes import (
    ImportCount as V41ImportCount,
)
from dhis2w_client.v41.envelopes import (
    WebMessageResponse as V41WebMessageResponse,
)


def test_v41_envelopes_imports_from_v41_generated_tree() -> None:
    """v41 envelopes wires its types from the v41 generated tree, not v42."""
    import dhis2w_client.v41.envelopes as envelopes_module

    for attr_name, expected_module in (
        ("ErrorReport", "dhis2w_client.generated.v41.oas.error_report"),
        ("ImportReport", "dhis2w_client.generated.v41.oas.import_report"),
        ("ObjectReport", "dhis2w_client.generated.v41.oas.object_report"),
        ("Stats", "dhis2w_client.generated.v41.oas.stats"),
        ("TypeReport", "dhis2w_client.generated.v41.oas.type_report"),
        ("WebMessage", "dhis2w_client.generated.v41.oas.web_message"),
    ):
        cls = getattr(envelopes_module, attr_name)
        assert cls.__module__ == expected_module, f"{attr_name}: expected {expected_module!r}, got {cls.__module__!r}"


def test_v41_local_stubs_are_locally_defined() -> None:
    """v41 ImportConflict + ImportCount stubs live in the v41 envelopes module."""
    assert V41ImportConflict.__module__ == "dhis2w_client.v41.envelopes"
    assert V41ImportCount.__module__ == "dhis2w_client.v41.envelopes"


def test_v41_import_conflict_parses_wire_payload() -> None:
    """v41 ImportConflict stub parses the same wire shape v42 + v43 emit."""
    conflict = V41ImportConflict.model_validate(
        {
            "errorCode": "E4003",
            "indexes": [2, 7],
            "object": "org.hisp.dhis.dataelement.DataElement",
            "property": "name",
            "value": "duplicate",
        }
    )
    assert conflict.errorCode == "E4003"
    assert conflict.indexes == [2, 7]
    assert conflict.property == "name"


def test_v41_import_count_parses_wire_payload() -> None:
    """v41 ImportCount stub parses the same wire shape v42 + v43 emit."""
    count = V41ImportCount.model_validate({"imported": 10, "updated": 2, "ignored": 1, "deleted": 0})
    assert count.imported == 10
    assert count.updated == 2
    assert count.ignored == 1
    assert count.deleted == 0


@respx.mock
async def test_top_level_client_against_v41_uses_v41_envelopes() -> None:
    """A top-level Dhis2Client talking to a v41 server uses the v41 envelope shapes."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="<html></html>"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.41.0"})
    )
    async with Dhis2Client(
        "https://dhis2.example",
        auth=BasicAuth(username="admin", password="district"),
        allow_version_fallback=True,
    ) as client:
        assert client.version_key == "v41"
        # The data_values accessor on a v41 server comes from the v41 tree.
        assert client.data_values.__class__.__module__ == "dhis2w_client.v41.data_values"
        # The v41 envelope module's WebMessageResponse is what v41 helpers return.
        envelope = V41WebMessageResponse.model_validate(
            {"httpStatus": "OK", "httpStatusCode": 200, "status": "OK", "response": {"imported": 5}}
        )
        count = envelope.import_count()
        assert count is not None
        assert count.imported == 5
        assert isinstance(count, V41ImportCount)
