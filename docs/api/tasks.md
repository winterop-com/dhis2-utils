# Tasks module

`client.tasks` — wait on DHIS2 background jobs (analytics refresh, metadata import, predictor runs, etc.). DHIS2's task endpoints (`/api/system/tasks/{jobType}` and `/api/system/taskSummaries/{jobType}`) report job progress as a stream of notification entries; the module polls them and resolves a `TaskCompletion` model when the job finishes.

```python
async with Dhis2Client(...) as client:
    # Kick off an analytics refresh — the maintenance accessor returns a task reference.
    task_ref = await client.maintenance.refresh_analytics_async()
    completion = await client.tasks.await_completion(task_ref, timeout=300)
    print(completion.status, completion.notifications[-1].message)
```

Two failure modes:

- `TaskTimeoutError` — the polling loop hit the `timeout` deadline before DHIS2 marked the job complete. The partial notification list is on the exception.
- Job-failure status — DHIS2 reports `status="ERROR"` or `status="FAILED"`. `await_completion` returns the typed `TaskCompletion`; callers branch on `.status`.

`parse_task_ref` converts the `{response: {id, jobType}}` envelope that DHIS2 returns from async-trigger endpoints into a usable reference for `await_completion`.

Worked example: [`examples/v42/client/task_await.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/task_await.py).

::: dhis2w_client.v42.tasks
