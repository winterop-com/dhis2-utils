"""Streaming `/api/analytics*` downloads — `client.analytics.stream_to`.

DHIS2's analytics endpoint family can return very large responses on
reasonable queries (every cell of a yearly district-level pivot against a
dozen data elements). Buffering the full JSON / CSV body into Python
memory before parsing is the slow path. `client.analytics.stream_to`
feeds httpx's `stream()` iterator to `response.aiter_bytes()` and writes
straight to disk — the body is never fully resident in the process.

Counterpart to `client.data_values.stream` (import side); this one handles
the export direction.

Endpoints covered (pass the full path including extension / sub-resource):

- `/api/analytics.json` (default)
- `/api/analytics.csv`
- `/api/analytics.xlsx`
- `/api/analytics/rawData.json` (requires `.json` suffix, see BUGS.md #1)
- `/api/analytics/dataValueSet.json` (same)
- `/api/analytics/events/query/<program>.json`

`params` is forwarded verbatim — DHIS2's repeated-param pattern
(`dimension=dx:...&dimension=pe:...&dimension=ou:...`) expects either a
mapping with list values (`{"dimension": ["dx:...", ...]}`) or a list of
2-tuples (`[("dimension", "dx:..."), ("dimension", "pe:...")]`).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import httpx

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


_DEFAULT_CHUNK_SIZE = 64 * 1024  # 64 KiB balances syscall count vs chunk overhead.

AnalyticsQuery = Mapping[str, Any] | Sequence[tuple[str, Any]]


class AnalyticsAccessor:
    """`Dhis2Client.analytics` — streaming downloads for the analytics endpoint family.

    Stateless wrapper around httpx's streaming GET. Stay here for exports
    large enough that buffering the whole body is a concern; the existing
    plugin-layer `dhis2_core.plugins.analytics.service.run_query` is the
    right call for small responses you want parsed into
    `AnalyticsResponse`.
    """

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def stream_to(
        self,
        destination: Path,
        *,
        params: AnalyticsQuery,
        endpoint: str = "/api/analytics.json",
        chunk_size: int = _DEFAULT_CHUNK_SIZE,
    ) -> int:
        """Stream a GET on `endpoint` straight to `destination`; return bytes written.

        `params` forwards exactly what DHIS2 accepts — use a list of
        2-tuples when you need repeated `dimension=` params, or a mapping
        whose values are lists when a key can appear more than once.

        `endpoint` is the full path including extension + sub-resource
        (`/api/analytics.csv`, `/api/analytics/rawData.json`, ...).
        `client.system.info()` uses the same httpx pool, so auth + retry +
        pool-tuning all still apply.

        Raises `Dhis2ApiError` on 4xx / 5xx (the error body is buffered —
        errors are small and readable).
        """
        headers = await self._client._auth.headers()  # noqa: SLF001 — accessor is tight with the client
        http = self._client._http  # noqa: SLF001
        if http is None:
            raise RuntimeError("Dhis2Client is not connected; call connect() first")

        destination.parent.mkdir(parents=True, exist_ok=True)
        bytes_written = 0
        # httpx.stream accepts a wider union than our typed StreamSource — cast
        # at the boundary rather than re-expressing DHIS2's repeated-key shape.
        query_params = cast(httpx._types.QueryParamTypes, params)
        async with http.stream("GET", endpoint, params=query_params, headers=headers) as response:
            if response.status_code >= 400:
                # 4xx / 5xx responses are small; buffer the body for the error.
                await response.aread()
                body: Any
                try:
                    body = response.json()
                except ValueError:
                    body = response.text
                from dhis2_client.errors import AuthenticationError, Dhis2ApiError

                if response.status_code == 401:
                    raise AuthenticationError(f"401 Unauthorized at GET {endpoint}")
                raise Dhis2ApiError(
                    status_code=response.status_code,
                    message=response.reason_phrase,
                    body=body,
                )
            with destination.open("wb") as handle:
                async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                    handle.write(chunk)
                    bytes_written += len(chunk)
        return bytes_written


__all__ = ["AnalyticsAccessor", "AnalyticsQuery"]
