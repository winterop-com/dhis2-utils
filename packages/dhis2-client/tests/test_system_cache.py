"""Tests for `SystemCache` + `client.system` cached accessors."""

from __future__ import annotations

import asyncio

import httpx
import pytest
import respx
from dhis2_client import BasicAuth, Dhis2Client, SystemCache


def _mock_preamble(version: str = "2.42.4") -> None:
    """Stub the canonical-URL + /api/system/info probes `Dhis2Client.connect()` performs."""
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": version}),
    )


def _auth() -> BasicAuth:
    """Build a throwaway BasicAuth for test clients."""
    return BasicAuth(username="a", password="b")


@respx.mock
async def test_connect_primes_system_info_cache_so_first_info_call_is_free() -> None:
    """After `connect()`, `system.info()` reuses the info response from connect itself."""
    _mock_preamble()

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        info = await client.system.info()
        info_again = await client.system.info()
    finally:
        await client.close()

    # Connect hit it once; neither info() call hit it again.
    assert respx.calls.call_count == 2  # root probe + /api/system/info on connect
    assert info.version == "2.42.4"
    assert info_again.version == "2.42.4"


@respx.mock
async def test_second_info_call_without_cache_hits_network() -> None:
    """`use_cache=False` forces a fresh fetch even when a cached entry exists."""
    _mock_preamble()

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        info_calls_before = len(
            [call for call in respx.calls if call.request.url.path == "/api/system/info"],
        )
        await client.system.info(use_cache=False)
        info_calls_after = len(
            [call for call in respx.calls if call.request.url.path == "/api/system/info"],
        )
    finally:
        await client.close()

    assert info_calls_after == info_calls_before + 1


@respx.mock
async def test_disabling_cache_bypasses_all_caching() -> None:
    """`system_cache_ttl=None` disables caching — every info() hits network."""
    _mock_preamble()

    client = Dhis2Client("https://dhis2.example", auth=_auth(), system_cache_ttl=None)
    try:
        await client.connect()
        await client.system.info()
        await client.system.info()
    finally:
        await client.close()

    info_calls = [call for call in respx.calls if call.request.url.path == "/api/system/info"]
    # One on connect + one per info() call = 3 total.
    assert len(info_calls) == 3
    assert client.system_cache is None


@respx.mock
async def test_invalidate_drops_cached_entries() -> None:
    """`invalidate_cache()` forces the next call back through the network."""
    _mock_preamble()

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        await client.system.info()  # cache hit (primed from connect)
        client.system.invalidate_cache()
        await client.system.info()  # refetch
    finally:
        await client.close()

    info_calls = [call for call in respx.calls if call.request.url.path == "/api/system/info"]
    assert len(info_calls) == 2


@respx.mock
async def test_default_category_combo_uid_caches_after_first_lookup() -> None:
    """Second call returns the cached UID without hitting `/api/categoryCombos` again."""
    _mock_preamble()
    route = respx.get("https://dhis2.example/api/categoryCombos").mock(
        return_value=httpx.Response(200, json={"categoryCombos": [{"id": "defaultCcUid"}]}),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        first = await client.system.default_category_combo_uid()
        second = await client.system.default_category_combo_uid()
    finally:
        await client.close()

    assert first == "defaultCcUid"
    assert second == "defaultCcUid"
    assert route.call_count == 1


@respx.mock
async def test_default_category_combo_uid_raises_when_missing() -> None:
    """A DHIS2 instance with no 'default' CC is broken — raise a clear error."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/categoryCombos").mock(
        return_value=httpx.Response(200, json={"categoryCombos": []}),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        with pytest.raises(RuntimeError, match="no categoryCombo named 'default'"):
            await client.system.default_category_combo_uid()
    finally:
        await client.close()


@respx.mock
async def test_setting_caches_per_key() -> None:
    """Different keys cache independently; same key dedupes."""
    _mock_preamble()
    title_route = respx.get("https://dhis2.example/api/systemSettings/applicationTitle").mock(
        return_value=httpx.Response(200, json={"applicationTitle": "My DHIS2"}),
    )
    intro_route = respx.get("https://dhis2.example/api/systemSettings/keyApplicationIntro").mock(
        return_value=httpx.Response(200, json={"keyApplicationIntro": "Welcome"}),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        title1 = await client.system.setting("applicationTitle")
        title2 = await client.system.setting("applicationTitle")
        intro = await client.system.setting("keyApplicationIntro")
    finally:
        await client.close()

    assert title1 == "My DHIS2"
    assert title2 == "My DHIS2"
    assert intro == "Welcome"
    assert title_route.call_count == 1
    assert intro_route.call_count == 1


@respx.mock
async def test_setting_returns_none_on_error_or_missing() -> None:
    """4xx/5xx OR an empty body → `None` (unset setting)."""
    _mock_preamble()
    respx.get("https://dhis2.example/api/systemSettings/missingKey").mock(
        return_value=httpx.Response(404, json={"message": "not found"}),
    )
    respx.get("https://dhis2.example/api/systemSettings/blankKey").mock(
        return_value=httpx.Response(200, json={}),
    )

    client = Dhis2Client("https://dhis2.example", auth=_auth())
    try:
        await client.connect()
        assert await client.system.setting("missingKey") is None
        assert await client.system.setting("blankKey") is None
    finally:
        await client.close()


async def test_cache_ttl_expires_after_interval() -> None:
    """A manually-constructed cache refetches after its TTL elapses."""
    cache = SystemCache(ttl=0.05)
    counter = {"n": 0}

    async def fetcher() -> int:
        counter["n"] += 1
        return counter["n"]

    first = await cache.get_or_fetch("key", fetcher)
    second = await cache.get_or_fetch("key", fetcher)  # still fresh
    await asyncio.sleep(0.1)
    third = await cache.get_or_fetch("key", fetcher)  # TTL elapsed

    assert first == 1
    assert second == 1
    assert third == 2


async def test_cache_dedupes_concurrent_fetches() -> None:
    """Fan-out of 10 gather tasks on the same key runs the fetcher once."""
    cache = SystemCache(ttl=10.0)
    calls = 0

    async def slow_fetcher() -> str:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.05)
        return "value"

    results = await asyncio.gather(
        *(cache.get_or_fetch("key", slow_fetcher) for _ in range(10)),
    )
    assert calls == 1
    assert results == ["value"] * 10


def test_cache_invalidate_accepts_specific_key_or_all() -> None:
    """`invalidate(key)` drops one entry; `invalidate()` drops everything."""
    cache = SystemCache(ttl=10.0)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.invalidate("a")
    cache.set("a", 3)  # re-prime after selective drop
    cache.invalidate()  # drop both
    # Nothing to assert on state directly — the public surface is get_or_fetch.
    # Exercise get_or_fetch to confirm both are gone.

    async def check() -> None:
        fetched_a = await cache.get_or_fetch("a", lambda: _const(99))
        fetched_b = await cache.get_or_fetch("b", lambda: _const(88))
        assert fetched_a == 99
        assert fetched_b == 88

    asyncio.run(check())


async def _const(value: int) -> int:
    """Tiny async const — async lambdas aren't valid Python."""
    return value
