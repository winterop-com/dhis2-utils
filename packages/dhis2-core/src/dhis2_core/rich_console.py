"""Module-level shared Rich stderr console.

Rich's live displays (`Progress`, `Status`, `Live`) and its logging bridge
(`RichHandler`) only play well together when they share one `Console` — each
instance has its own lock that the others don't see. Every `--watch` UI and
every debug log line goes through `STDERR_CONSOLE` so they render without
tearing when both are active at once.
"""

from __future__ import annotations

from rich.console import Console

STDERR_CONSOLE = Console(stderr=True)
