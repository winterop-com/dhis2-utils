"""Streaming data-value-set import — `client.data_values.stream`.

DHIS2's `POST /api/dataValueSets` accepts JSON, XML, CSV, and ADX payloads.
For a 100k-row push (a typical month-end aggregate upload), buffering the
whole body in Python memory before the POST is the thing to avoid:

- A 100k-row JSON payload sits at ~30-60 MB on the wire, and the Python
  parsed shape is 3-5x that — so ~150 MB resident just to stage the
  request.
- The same payload on CSV is ~8 MB; XML is in between.

`client.data_values.stream(source, content_type)` feeds httpx's chunked
transfer encoding directly, so the payload never sits fully in memory
on the client side. The server consumes it as it arrives.

`source` accepts any of:

- `pathlib.Path` — opens the file and chunks it through.
- `bytes` / `bytearray` — single-shot for callers who already have the
  body assembled but want the typed `WebMessageResponse` envelope.
- `Iterable[bytes]` / `AsyncIterable[bytes]` — pass-through for
  generators that build the body on the fly (e.g. DB-row → CSV line).
- File-like with `.read(size) -> bytes` (sync or async) — adapted to a
  chunk iterator.

Supported `content_type` values map to the DHIS2-accepted MIME types:

- `application/json` (default)
- `application/xml`
- `application/csv` (also accepted: `text/csv`)
- `application/adx+xml`
"""

from __future__ import annotations

from collections.abc import AsyncIterable, AsyncIterator, Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from dhis2w_client.v42.envelopes import WebMessageResponse

if TYPE_CHECKING:
    from dhis2w_client.v42.client import Dhis2Client


_DEFAULT_CHUNK_SIZE = 64 * 1024  # 64 KiB — balances syscall count vs chunk overhead.

StreamSource = Path | bytes | bytearray | memoryview | Iterable[bytes] | AsyncIterable[bytes]


class DataValuesAccessor:
    """`Dhis2Client.data_values` — streaming uploads to `/api/dataValueSets`.

    Stateless wrapper over the streaming POST path. Stay here for the large
    import cases; use `dhis2w_core.plugins.aggregate.service.push_data_values`
    when the payload is already a small in-memory list of typed data values.
    """

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def stream(
        self,
        source: StreamSource,
        *,
        content_type: str = "application/json",
        dry_run: bool = False,
        preheat_cache: bool = True,
        import_strategy: str | None = None,
        id_scheme: str | None = None,
        data_element_id_scheme: str | None = None,
        org_unit_id_scheme: str | None = None,
        skip_audit: bool = False,
        async_job: bool = False,
        chunk_size: int = _DEFAULT_CHUNK_SIZE,
    ) -> WebMessageResponse:
        """Stream `source` to `POST /api/dataValueSets` and return the typed envelope.

        `content_type` picks which DHIS2 parser handles the body (JSON / XML /
        CSV / ADX). Every param from the standard `/api/dataValueSets` surface
        is forwarded via query string:

        - `dry_run` → `dryRun=true`: validate without committing.
        - `preheat_cache=False` → `preheatCache=false`.
        - `import_strategy`: `CREATE` / `UPDATE` / `CREATE_AND_UPDATE` / `DELETE`.
        - `id_scheme` / `data_element_id_scheme` / `org_unit_id_scheme`: pick
          the identifier scheme for the payload (`UID` / `CODE` / `NAME` / ...).
        - `skip_audit=True` → `skipAudit=true`.
        - `async_job=True` → `async=true`: DHIS2 queues the import as a job
          and the returned envelope carries `response.jobType` / `response.id`.
          Poll with `client.tasks.await_completion(envelope.task_ref())`.

        Returns a `WebMessageResponse`. For synchronous imports,
        `envelope.import_count()` gives `ImportCount.imported / updated /
        ignored / deleted`; `envelope.conflicts()` lists per-row rejections.
        Async imports return the task-ref envelope — poll it to completion
        to get the final report from DHIS2.
        """
        params: dict[str, Any] = {}
        if dry_run:
            params["dryRun"] = "true"
        if not preheat_cache:
            params["preheatCache"] = "false"
        if import_strategy is not None:
            params["importStrategy"] = import_strategy
        if id_scheme is not None:
            params["idScheme"] = id_scheme
        if data_element_id_scheme is not None:
            params["dataElementIdScheme"] = data_element_id_scheme
        if org_unit_id_scheme is not None:
            params["orgUnitIdScheme"] = org_unit_id_scheme
        if skip_audit:
            params["skipAudit"] = "true"
        if async_job:
            params["async"] = "true"

        content = _coerce_stream_source(source, chunk_size=chunk_size)
        response = await self._client._request(  # noqa: SLF001 — accessor is intentionally tight with the client
            "POST",
            "/api/dataValueSets",
            params=params,
            content=content,
            extra_headers={"Content-Type": content_type},
        )
        raw = response.json() if response.content else {}
        return WebMessageResponse.model_validate(raw)


def _coerce_stream_source(source: StreamSource, *, chunk_size: int) -> bytes | AsyncIterable[bytes]:
    """Map `StreamSource` to an httpx-compatible `content=` shape.

    `httpx.AsyncClient` requires streamed bodies to be `AsyncIterable[bytes]`
    (sync iterables are rejected). Every non-bytes source normalises to an
    async iterator that yields chunks; single-shot bytes pass through
    unchanged for the common "already have the body" case.
    """
    if isinstance(source, Path):
        return _async_file_chunks(source, chunk_size=chunk_size)
    if isinstance(source, (bytes, bytearray, memoryview)):
        return bytes(source)
    if isinstance(source, AsyncIterable):
        return _passthrough_async(source)
    if isinstance(source, Iterable):  # pyright: ignore[reportUnnecessaryIsInstance]
        return _sync_to_async(source)
    # Runtime fallback for callers that bypass the StreamSource type annotation.
    raise TypeError(
        f"unsupported stream source type: {type(source).__name__}. "
        "Pass a pathlib.Path, bytes, Iterable[bytes], or AsyncIterable[bytes].",
    )


async def _async_file_chunks(path: Path, *, chunk_size: int) -> AsyncIterator[bytes]:
    """Yield `chunk_size` bytes at a time from `path` via an async iterator.

    File IO itself is synchronous (Python's stdlib can't do true async file
    reads without `aiofiles`); the async iterator surface is what httpx's
    streamed-upload path requires.
    """
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                return
            yield chunk


def _sync_to_async(source: Iterable[bytes]) -> AsyncIterator[bytes]:
    """Wrap a sync iterable as async — needed for httpx.AsyncClient streaming."""

    async def _generator() -> AsyncIterator[bytes]:
        for chunk in source:
            yield bytes(chunk)

    return _generator()


async def _passthrough_async(source: AsyncIterable[bytes]) -> AsyncIterator[bytes]:
    """Adapt an async iterable into one that httpx consumes."""
    async for chunk in source:
        yield bytes(chunk)


__all__ = ["DataValuesAccessor", "StreamSource"]
