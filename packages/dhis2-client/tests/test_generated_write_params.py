"""Tests for the generated CRUD `create` / `update` write-flag params + the
per-item collection shortcut helpers (`add_collection_item` /
`remove_collection_item`)."""

from __future__ import annotations

import httpx
import pytest
import respx
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.generated import available_versions, load

_GENERATED = available_versions()
pytestmark = pytest.mark.skipif(not _GENERATED, reason="no generated module populated")


def _wired_client() -> Dhis2Client:
    """Build a connected client without touching the network."""
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    generated = load(_GENERATED[-1])
    client._resources = generated.Resources(client)
    return client


@respx.mock
async def test_update_forwards_merge_mode_param() -> None:
    generated = load(_GENERATED[-1])
    route = respx.put("https://dhis2.example/api/dataElements/DE1").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    client = _wired_client()
    try:
        de = generated.DataElement(id="DE1", name="x")
        await client.resources.data_elements.update(de, merge_mode="REPLACE")
    finally:
        await client.close()
    assert route.calls.last.request.url.params["mergeMode"] == "REPLACE"


@respx.mock
async def test_create_forwards_every_write_flag() -> None:
    generated = load(_GENERATED[-1])
    route = respx.post("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(201, json={"status": "OK"}),
    )
    client = _wired_client()
    try:
        de = generated.DataElement(name="x")
        await client.resources.data_elements.create(
            de,
            merge_mode="REPLACE",
            import_strategy="CREATE_AND_UPDATE",
            skip_sharing=True,
            skip_translation=False,
        )
    finally:
        await client.close()
    params = route.calls.last.request.url.params
    assert params["mergeMode"] == "REPLACE"
    assert params["importStrategy"] == "CREATE_AND_UPDATE"
    assert params["skipSharing"] == "true"
    assert params["skipTranslation"] == "false"


@respx.mock
async def test_update_omits_params_when_no_flags_set() -> None:
    generated = load(_GENERATED[-1])
    route = respx.put("https://dhis2.example/api/dataElements/DE1").mock(
        return_value=httpx.Response(200, json={"status": "OK"}),
    )
    client = _wired_client()
    try:
        de = generated.DataElement(id="DE1", name="x")
        await client.resources.data_elements.update(de)
    finally:
        await client.close()
    assert not route.calls.last.request.url.query


@respx.mock
async def test_add_collection_item_posts_the_shortcut_path() -> None:
    route = respx.post(
        "https://dhis2.example/api/organisationUnitGroups/OUG1/organisationUnits/OU_A",
    ).mock(return_value=httpx.Response(204, json={}))
    client = _wired_client()
    try:
        await client.resources.organisation_unit_groups.add_collection_item(
            "OUG1",
            "organisationUnits",
            "OU_A",
        )
    finally:
        await client.close()
    assert route.called


@respx.mock
async def test_remove_collection_item_deletes_the_shortcut_path() -> None:
    route = respx.delete(
        "https://dhis2.example/api/indicatorGroups/IG1/indicators/IND_A",
    ).mock(return_value=httpx.Response(204, json={}))
    client = _wired_client()
    try:
        await client.resources.indicator_groups.remove_collection_item(
            "IG1",
            "indicators",
            "IND_A",
        )
    finally:
        await client.close()
    assert route.called
