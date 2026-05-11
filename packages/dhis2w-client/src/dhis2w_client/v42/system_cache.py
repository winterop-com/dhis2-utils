"""TTL-bounded in-memory cache for system-level reads on a single `Dhis2Client`.

Scoped to one client instance (not shared across clients). For scripts that
reuse one client for many reads, the cache kicks in on the second call of
each cached endpoint — `/api/system/info`, the default categoryCombo UID,
and per-key system-setting reads.

Concurrency: a per-key `asyncio.Lock` dedupes in-flight fetches so a fan-out
of 100 `asyncio.gather` tasks triggers one network call, not 100.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import BaseModel, ConfigDict


class _CacheEntry(BaseModel):
    """One cached value + its absolute expiry time (`time.monotonic` units)."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    value: Any
    expires_at: float


class SystemCache:
    """Per-client TTL cache for system-level reads.

    `ttl` is the max age (seconds) of any cached entry before the next read
    triggers a refetch. Entries never evict on their own — on a long-lived
    client, call `invalidate()` when you know the upstream changed
    (rename via the Admin UI, settings update through another process, etc.).
    """

    def __init__(self, ttl: float) -> None:
        """Bind the TTL; start with an empty store."""
        self._ttl = ttl
        self._store: dict[str, _CacheEntry] = {}
        self._locks: dict[str, asyncio.Lock] = {}

    @property
    def ttl(self) -> float:
        """Max age (seconds) for any cached entry before the next read refetches."""
        return self._ttl

    def _lock_for(self, key: str) -> asyncio.Lock:
        """Lazily create one lock per key — dedupes in-flight fetches for the same key."""
        lock = self._locks.get(key)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[key] = lock
        return lock

    async def get_or_fetch[T](self, key: str, fetcher: Callable[[], Awaitable[T]]) -> T:
        """Return a fresh cached value, or run `fetcher()` and cache its result."""
        now = time.monotonic()
        entry = self._store.get(key)
        if entry is not None and entry.expires_at > now:
            return entry.value  # type: ignore[no-any-return]
        async with self._lock_for(key):
            # Re-check under the lock — a concurrent task may have populated it.
            entry = self._store.get(key)
            now = time.monotonic()
            if entry is not None and entry.expires_at > now:
                return entry.value  # type: ignore[no-any-return]
            value = await fetcher()
            self._store[key] = _CacheEntry(value=value, expires_at=now + self._ttl)
            return value

    def set(self, key: str, value: Any) -> None:
        """Prime the cache — used by `connect()` to avoid a second round-trip to `/api/system/info`."""
        self._store[key] = _CacheEntry(value=value, expires_at=time.monotonic() + self._ttl)

    def invalidate(self, key: str | None = None) -> None:
        """Drop one key (when `key` is set) or every key (when `key is None`)."""
        if key is None:
            self._store.clear()
        else:
            self._store.pop(key, None)


__all__ = ["SystemCache"]
