# Maintenance

`MaintenanceAccessor` on `Dhis2Client.maintenance` — async background-job triggers (analytics refresh, monitoring refresh, resource-table regeneration, predictor + validation runs, cache clears) plus the data-integrity check / result / report typed surface.

## When to reach for it

- Programmatically refresh analytics or monitoring tables after a sync / migration completes (otherwise downstream queries hit stale data).
- Run DHIS2's built-in data-integrity scan (81 checks) before / after a big metadata import.
- Stream tagged integrity issues as they're emitted (large instances can have thousands; `iter_integrity_issues` is the streaming consumer).
- Clear server-side caches after a metadata change.

## Worked example — refresh analytics + watch the task

```python
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    # 1. Kick off analytics-table regeneration. Returns immediately
    #    with a TaskRef; DHIS2 runs the regen on a background thread.
    task_ref = await client.maintenance.refresh_analytics_async()

    # 2. Poll until complete (the convenience `await_completion` wraps
    #    `client.tasks.await_completion` with sensible defaults).
    completion = await client.maintenance.await_task(task_ref, timeout=600)
    print(f"status={completion.status}  notifications={len(completion.notifications)}")
    if completion.status not in {"COMPLETED", "SUCCESS"}:
        for n in completion.notifications[-5:]:
            print(f"  {n.level}: {n.message}")
```

## Worked example — stream integrity issues

```python
async with open_client(profile_from_env()) as client:
    # `iter_integrity_issues` is an async iterator — one DataIntegrityResult
    # per row as DHIS2 emits it; safe for instances with thousands of issues.
    severity_counts: dict[str, int] = {}
    async for issue in client.maintenance.iter_integrity_issues():
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        if severity_counts.get(issue.severity, 0) <= 3:
            print(f"  [{issue.severity}] {issue.name}: {issue.description}")
    print(f"total by severity: {severity_counts}")
```

## Related examples

- [`examples/v42/client/task_polling.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/task_polling.py) — explicit `client.tasks.await_completion` against an analytics refresh.
- [`examples/v42/client/integrity_issues_stream.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/integrity_issues_stream.py) — `iter_integrity_issues` + severity histogram + early-break scan.

::: dhis2w_client.v42.maintenance
