"""URL-construction tests for the generated list() accessor query params."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlparse

import httpx
import pytest
import respx
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.generated import available_versions, load

_GENERATED = available_versions()
pytestmark = pytest.mark.skipif(not _GENERATED, reason="no generated module populated")


def _sent_query(route: respx.Route) -> list[tuple[str, str]]:
    """Parse the last request's query string into key/value pairs, order-preserving."""
    assert route.called, "expected the mocked route to be hit"
    url = str(route.calls.last.request.url)
    return parse_qsl(urlparse(url).query, keep_blank_values=True)


async def _make_client() -> Dhis2Client:
    generated = load(_GENERATED[-1])
    client = Dhis2Client("https://dhis2.example", auth=BasicAuth(username="a", password="b"))
    client._http = httpx.AsyncClient(base_url="https://dhis2.example")
    client._resources = generated.Resources(client)
    return client


@respx.mock
async def test_single_filter_emits_one_param() -> None:
    route = respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(200, json={"dataElements": []}),
    )
    client = await _make_client()
    try:
        await client.resources.data_elements.list(filters=["name:like:Malaria"])
    finally:
        await client.close()
    assert _sent_query(route) == [("filter", "name:like:Malaria"), ("paging", "false")]


@respx.mock
async def test_multiple_filters_emit_repeated_params() -> None:
    route = respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(200, json={"dataElements": []}),
    )
    client = await _make_client()
    try:
        await client.resources.data_elements.list(
            filters=["name:like:ANC", "code:eq:DEancVisit1"],
            root_junction="OR",
        )
    finally:
        await client.close()
    query = _sent_query(route)
    assert ("filter", "name:like:ANC") in query
    assert ("filter", "code:eq:DEancVisit1") in query
    assert ("rootJunction", "OR") in query


@respx.mock
async def test_order_emits_repeated_params() -> None:
    route = respx.get("https://dhis2.example/api/organisationUnits").mock(
        return_value=httpx.Response(200, json={"organisationUnits": []}),
    )
    client = await _make_client()
    try:
        await client.resources.organisation_units.list(order=["level:asc", "name:asc"])
    finally:
        await client.close()
    query = _sent_query(route)
    assert ("order", "level:asc") in query
    assert ("order", "name:asc") in query


@respx.mock
async def test_page_and_page_size() -> None:
    route = respx.get("https://dhis2.example/api/indicators").mock(
        return_value=httpx.Response(200, json={"indicators": []}),
    )
    client = await _make_client()
    try:
        await client.resources.indicators.list(page=3, page_size=25, paging=True)
    finally:
        await client.close()
    query = dict(_sent_query(route))
    assert query["page"] == "3"
    assert query["pageSize"] == "25"
    assert query["paging"] == "true"


@respx.mock
async def test_paging_false_default() -> None:
    route = respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(200, json={"dataElements": []}),
    )
    client = await _make_client()
    try:
        # No `paging` arg -> list() defaults to False for the single-call shape.
        await client.resources.data_elements.list()
    finally:
        await client.close()
    assert ("paging", "false") in _sent_query(route)


@respx.mock
async def test_paging_true_explicit() -> None:
    route = respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(200, json={"dataElements": []}),
    )
    client = await _make_client()
    try:
        await client.resources.data_elements.list(paging=True)
    finally:
        await client.close()
    assert ("paging", "true") in _sent_query(route)


@respx.mock
async def test_translate_and_locale() -> None:
    route = respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(200, json={"dataElements": []}),
    )
    client = await _make_client()
    try:
        await client.resources.data_elements.list(translate=True, locale="fr")
    finally:
        await client.close()
    query = dict(_sent_query(route))
    assert query["translate"] == "true"
    assert query["locale"] == "fr"


@respx.mock
async def test_fields_preset_passthrough() -> None:
    route = respx.get("https://dhis2.example/api/dataElements").mock(
        return_value=httpx.Response(200, json={"dataElements": []}),
    )
    client = await _make_client()
    try:
        await client.resources.data_elements.list(fields=":identifiable")
    finally:
        await client.close()
    assert ("fields", ":identifiable") in _sent_query(route)


@respx.mock
async def test_list_raw_returns_pager_block() -> None:
    respx.get("https://dhis2.example/api/indicators").mock(
        return_value=httpx.Response(
            200,
            json={
                "pager": {"page": 1, "pageCount": 2, "total": 3, "pageSize": 2},
                "indicators": [{"id": "a"}, {"id": "b"}],
            },
        ),
    )
    client = await _make_client()
    try:
        raw = await client.resources.indicators.list_raw(paging=True, page_size=2)
    finally:
        await client.close()
    assert raw["pager"]["total"] == 3
    assert len(raw["indicators"]) == 2
