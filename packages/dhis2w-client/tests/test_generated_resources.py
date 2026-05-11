"""Unit tests for the generated CRUD resource accessors against the highest available version."""

from __future__ import annotations

import httpx
import pytest
import respx
from dhis2w_client import BasicAuth, Dhis2Client
from dhis2w_client.generated import available_versions, load

_GENERATED = available_versions()
pytestmark = pytest.mark.skipif(not _GENERATED, reason="no generated module populated")


@respx.mock
async def test_get_data_element_typed() -> None:
    """Get data element typed."""
    generated = load(_GENERATED[-1])
    respx.get("https://dhis2.example/api/dataElements/abc123").mock(
        return_value=httpx.Response(200, json={"id": "abc123", "name": "Malaria Cases"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    client._resources = generated.Resources(client)
    try:
        de = await client.resources.data_elements.get("abc123")
    finally:
        await client.close()
    assert de.id == "abc123"
    assert de.name == "Malaria Cases"


@respx.mock
async def test_list_data_elements_returns_typed_models() -> None:
    """List data elements returns typed models."""
    generated = load(_GENERATED[-1])
    respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(
            200,
            json={"dataElements": [{"id": "a"}, {"id": "b"}, {"id": "c"}]},
        ),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    client._resources = generated.Resources(client)
    try:
        items = await client.resources.data_elements.list()
    finally:
        await client.close()
    assert len(items) == 3
    assert [x.id for x in items] == ["a", "b", "c"]


@respx.mock
async def test_create_data_element_posts() -> None:
    """Create data element posts."""
    generated = load(_GENERATED[-1])
    route = respx.post("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(201, json={"status": "OK", "response": {"uid": "new123"}}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    client._resources = generated.Resources(client)

    module = __import__(f"dhis2w_client.generated.{_GENERATED[-1]}.schemas.data_element", fromlist=["DataElement"])
    new_item = module.DataElement(name="Test DE", shortName="Test")
    try:
        response = await client.resources.data_elements.create(new_item)
    finally:
        await client.close()
    assert response["status"] == "OK"
    assert route.called


@respx.mock
async def test_update_data_element_puts_with_id() -> None:
    """Update data element puts with id."""
    generated = load(_GENERATED[-1])
    route = respx.put("https://dhis2.example/api/dataElements/abc123").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    client._resources = generated.Resources(client)

    module = __import__(f"dhis2w_client.generated.{_GENERATED[-1]}.schemas.data_element", fromlist=["DataElement"])
    existing = module.DataElement(id="abc123", name="Updated")
    try:
        await client.resources.data_elements.update(existing)
    finally:
        await client.close()
    assert route.called


async def test_update_raises_without_id() -> None:
    """Update raises without id."""
    generated = load(_GENERATED[-1])
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    client._resources = generated.Resources(client)

    module = __import__(f"dhis2w_client.generated.{_GENERATED[-1]}.schemas.data_element", fromlist=["DataElement"])
    without_id = module.DataElement(name="no-id")
    try:
        with pytest.raises(ValueError, match="id is required"):
            await client.resources.data_elements.update(without_id)
    finally:
        await client.close()


@respx.mock
async def test_delete_data_element() -> None:
    """Delete data element."""
    generated = load(_GENERATED[-1])
    route = respx.delete("https://dhis2.example/api/dataElements/abc123").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    client._resources = generated.Resources(client)
    try:
        await client.resources.data_elements.delete("abc123")
    finally:
        await client.close()
    assert route.called
