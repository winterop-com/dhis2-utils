"""Background-task polling — watch a `/api/resourceTables/analytics` job to done.

Every async DHIS2 op returns a `JobConfigurationWebMessageResponse` with
`response.jobType` and `response.id`. `WebMessageResponse.task_ref()` pulls
the `(job_type, task_uid)` tuple; `maintenance.service.watch_task` polls
`/api/system/tasks/{type}/{uid}` until the job reports `completed=true`.

Usage:
    uv run python examples/client/16_task_polling.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth, WebMessageResponse


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


async def _poll_task(client: Dhis2Client, job_type: str, task_uid: str, interval: float = 1.0) -> None:
    """Poll `/api/system/tasks/{job_type}/{task_uid}` until completed=true.

    This mirrors `dhis2_core.plugins.maintenance.service.watch_task` but uses
    only the library client (no dhis2-core dependency) so it's copy-paste-able
    into any dhis2-client project.
    """
    seen: set[str] = set()
    while True:
        raw = await client.get_raw(f"/api/system/tasks/{job_type}/{task_uid}")
        notifications: list[dict[str, Any]] = raw.get("data", []) if "data" in raw else []
        # DHIS2 returns newest-first; walk chronologically.
        for notification in reversed(notifications):
            identifier = str(notification.get("uid") or notification.get("id") or notification.get("time") or "")
            if identifier in seen:
                continue
            seen.add(identifier)
            level = notification.get("level", "INFO")
            message = notification.get("message", "-")
            completed = notification.get("completed", False)
            marker = "[x]" if completed else "[ ]"
            print(f"  {level:<5} {marker} {message}")
            if completed:
                return
        await asyncio.sleep(interval)


async def main() -> None:
    """Kick off an analytics refresh and stream its notifications."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        print("kicking off POST /api/resourceTables/analytics (lastYears=1)")
        raw = await client.post_raw("/api/resourceTables/analytics", params={"lastYears": 1})
        envelope = WebMessageResponse.model_validate(raw)
        ref = envelope.task_ref()
        if ref is None:
            print("  response had no jobType/id — can't watch")
            return
        job_type, task_uid = ref
        print(f"  kicked off {job_type}/{task_uid} — streaming notifications...\n")
        await _poll_task(client, job_type, task_uid, interval=1.0)


if __name__ == "__main__":
    asyncio.run(main())
