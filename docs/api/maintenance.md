# Maintenance

`MaintenanceAccessor` on `Dhis2Client.maintenance` — async background-job triggers (analytics refresh, monitoring refresh, resource-table regeneration, predictor + validation runs, cache clears) plus the data-integrity check / result / report typed surface.

## When to reach for it

- Programmatically refresh analytics or monitoring tables after a sync / migration completes (otherwise downstream queries hit stale data).
- Run DHIS2's built-in data-integrity scan (81 checks) before / after a big metadata import.
- Stream tagged integrity issues as they're emitted (large instances can have thousands; `iter_integrity_issues` is the streaming consumer).
- Clear server-side caches after a metadata change.

## Worked example — stream integrity issues

```python
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    # `iter_integrity_issues` is an async iterator — one `IntegrityIssueRow`
    # per row as DHIS2 emits it; safe for instances with thousands of issues.
    severity_counts: dict[str, int] = {}
    async for issue in client.maintenance.iter_integrity_issues():
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        if severity_counts.get(issue.severity, 0) <= 3:
            print(f"  [{issue.severity}] {issue.name}: {issue.description}")
    print(f"total by severity: {severity_counts}")
```

## Worked example — full integrity report (snapshot, not stream)

```python
async with open_client(profile_from_env()) as client:
    report = await client.maintenance.get_integrity_report()
    print(f"checks ran: {len(report.checks)}, issues found: {len(report.issues)}")
    for check in report.checks[:5]:
        print(f"  {check.name}: {check.severity}")
```

## Triggering analytics / monitoring refresh

The accessor doesn't expose a refresh trigger directly — refresh is a plugin-service surface, not a raw-client one. Three real paths:

1. **CLI**: `dhis2 maintenance refresh analytics --watch`.
2. **MCP**: `maintenance_refresh_analytics` tool with `watch=true`.
3. **Python via plugin service**: import `dhis2w_core.v42.plugins.maintenance.service.refresh_analytics(profile, ...)` directly — see [`examples/v42/client/task_polling.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/task_polling.py) for the full kick-off + poll-with-`client.tasks.await_completion` pattern.

## Related examples

- [`examples/v42/client/task_polling.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/task_polling.py) — kick off an analytics refresh via raw `client.post_raw("/api/resourceTables/analytics", ...)` + block on it with `client.tasks.await_completion`.
- [`examples/v42/client/integrity_issues_stream.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/integrity_issues_stream.py) — `iter_integrity_issues` + severity histogram + early-break scan.

::: dhis2w_client.v42.maintenance
