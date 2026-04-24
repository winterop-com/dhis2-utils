# Retry policy

`RetryPolicy` opts the client into transient-failure retries. Default-off — pass
`retry_policy=RetryPolicy(...)` to `Dhis2Client` and the underlying httpx
transport gets wrapped with exponential backoff, jitter, and `Retry-After`
support.

Only idempotent methods (GET, HEAD, PUT, DELETE, OPTIONS) retry by default. Set
`retry_non_idempotent=True` to also retry POST and PATCH — leave it off unless
the specific endpoint is known to be idempotent.

::: dhis2_client.retry
