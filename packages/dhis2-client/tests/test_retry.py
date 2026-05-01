"""Tests for `RetryPolicy` + `_RetryTransport` wiring into `Dhis2Client`."""

from __future__ import annotations

import random

import httpx
import pytest
import respx
from dhis2_client import BasicAuth, Dhis2Client, RetryPolicy
from dhis2_client.errors import Dhis2ApiError
from dhis2_client.retry import _RetryTransport, build_retry_transport


def test_retry_policy_defaults_are_sensible() -> None:
    """Default policy retries 3 attempts on 429/502/503/504, idempotent methods only."""
    policy = RetryPolicy()
    assert policy.max_attempts == 3
    assert policy.retry_statuses == frozenset({429, 502, 503, 504})
    assert policy.retry_non_idempotent is False
    assert policy.base_delay == 0.5


def test_compute_delay_scales_exponentially_without_jitter() -> None:
    """Exponential backoff with jitter=0 is deterministic."""
    policy = RetryPolicy(base_delay=0.1, backoff_factor=2.0, jitter=0.0, max_delay=10.0)
    assert policy.compute_delay(1) == pytest.approx(0.1)
    assert policy.compute_delay(2) == pytest.approx(0.2)
    assert policy.compute_delay(3) == pytest.approx(0.4)
    assert policy.compute_delay(10) == 10.0  # capped at max_delay


def test_compute_delay_jitter_stays_within_band() -> None:
    """Jitter keeps delays in [nominal*(1-jitter), nominal*(1+jitter)]."""
    policy = RetryPolicy(base_delay=1.0, backoff_factor=1.0, jitter=0.2, max_delay=10.0)
    rng = random.Random(42)
    for _ in range(100):
        delay = policy.compute_delay(1, rng=rng)
        assert 0.8 <= delay <= 1.2


@respx.mock
async def test_retry_on_503_succeeds_on_second_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    """GET that 503s once then 200s comes back OK through the retry transport."""

    async def _instant_sleep(_: float) -> None:
        return None

    monkeypatch.setattr("dhis2_client.retry.asyncio.sleep", _instant_sleep)
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )
    # Test retry against a separate endpoint so the connect-time /api/system/info probe
    # stays deterministic and one call deep.
    route = respx.get("https://dhis2.example/api/dataElements").mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(200, json={"dataElements": [{"id": "abc"}]}),
        ]
    )

    client = Dhis2Client(
        "https://dhis2.example",
        auth=BasicAuth(username="a", password="b"),
        retry_policy=RetryPolicy(base_delay=0.0, jitter=0.0),
    )
    try:
        await client.connect()
        body = await client.get_raw("/api/dataElements")
    finally:
        await client.close()
    assert body["dataElements"] == [{"id": "abc"}]
    assert route.call_count == 2  # first attempt 503, retry succeeded


@respx.mock
async def test_retry_exhaustion_raises_final_status(monkeypatch: pytest.MonkeyPatch) -> None:
    """When every attempt hits a retriable status, the client surfaces the final response as Dhis2ApiError."""

    async def _instant_sleep(_: float) -> None:
        return None

    monkeypatch.setattr("dhis2_client.retry.asyncio.sleep", _instant_sleep)
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )
    route = respx.get("https://dhis2.example/api/metadata").mock(
        return_value=httpx.Response(503, json={"httpStatus": "Service Unavailable"}),
    )

    client = Dhis2Client(
        "https://dhis2.example",
        auth=BasicAuth(username="a", password="b"),
        retry_policy=RetryPolicy(max_attempts=3, base_delay=0.0, jitter=0.0),
    )
    try:
        await client.connect()
        with pytest.raises(Dhis2ApiError) as exc:
            await client.get_raw("/api/metadata")
    finally:
        await client.close()
    assert exc.value.status_code == 503
    assert route.call_count == 3  # 3 attempts, all 503 — then raises


@respx.mock
async def test_post_is_not_retried_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """POSTs skip retry by default — double-writes risk DHIS2-side duplicates."""

    async def _instant_sleep(_: float) -> None:
        return None

    monkeypatch.setattr("dhis2_client.retry.asyncio.sleep", _instant_sleep)
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )
    route = respx.post("https://dhis2.example/api/metadata").mock(
        return_value=httpx.Response(503, json={"httpStatus": "Service Unavailable"}),
    )

    client = Dhis2Client(
        "https://dhis2.example",
        auth=BasicAuth(username="a", password="b"),
        retry_policy=RetryPolicy(max_attempts=3, base_delay=0.0, jitter=0.0),
    )
    try:
        await client.connect()
        with pytest.raises(Dhis2ApiError):
            await client.post_raw("/api/metadata", {"x": 1})
    finally:
        await client.close()
    assert route.call_count == 1  # no retry on non-idempotent method


@respx.mock
async def test_retry_non_idempotent_opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    """`retry_non_idempotent=True` retries POST/PATCH too — for endpoints the caller knows are safe."""

    async def _instant_sleep(_: float) -> None:
        return None

    monkeypatch.setattr("dhis2_client.retry.asyncio.sleep", _instant_sleep)
    respx.get("https://dhis2.example/").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("https://dhis2.example/api/system/info").mock(
        return_value=httpx.Response(200, json={"version": "2.42.4"}),
    )
    route = respx.post("https://dhis2.example/api/resourceTables/analytics").mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(503),
            httpx.Response(200, json={"status": "OK"}),
        ]
    )

    client = Dhis2Client(
        "https://dhis2.example",
        auth=BasicAuth(username="a", password="b"),
        retry_policy=RetryPolicy(max_attempts=3, base_delay=0.0, jitter=0.0, retry_non_idempotent=True),
    )
    try:
        await client.connect()
        result = await client.post_raw("/api/resourceTables/analytics")
    finally:
        await client.close()
    assert route.call_count == 3
    assert result["status"] == "OK"


async def test_retry_respects_retry_after_header(monkeypatch: pytest.MonkeyPatch) -> None:
    """A server `Retry-After` header overrides the computed backoff for that attempt."""
    sleep_args: list[float] = []

    async def tracked_sleep(seconds: float) -> None:
        sleep_args.append(seconds)

    monkeypatch.setattr("dhis2_client.retry.asyncio.sleep", tracked_sleep)

    policy = RetryPolicy(max_attempts=3, base_delay=0.5, jitter=0.0)
    transport = build_retry_transport(
        policy,
        inner=_FakeTransport(
            response_queue=[
                httpx.Response(503, headers={"Retry-After": "7"}),
                httpx.Response(200, text="ok"),
            ]
        ),
    )

    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get("https://dhis2.example/x")
    assert response.status_code == 200
    assert sleep_args == [7.0]  # server's Retry-After hint beats the computed 0.5


def test_retry_transport_is_async_base_transport() -> None:
    """The wrapper is a proper httpx transport so `httpx.AsyncClient(transport=...)` accepts it."""
    policy = RetryPolicy()
    transport = build_retry_transport(policy)
    assert isinstance(transport, _RetryTransport)
    assert isinstance(transport, httpx.AsyncBaseTransport)


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


class _FakeTransport(httpx.AsyncBaseTransport):
    """Return a queue of pre-built responses in order; used to drive retry-transport tests."""

    def __init__(self, *, response_queue: list[httpx.Response]) -> None:
        """Seed the queue."""
        self._queue = list(response_queue)

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """Pop the next response, or raise if the queue is empty."""
        if not self._queue:
            raise AssertionError("FakeTransport response queue exhausted")
        return self._queue.pop(0)

    async def aclose(self) -> None:
        """No-op; nothing owns resources on this fake."""
        return None
