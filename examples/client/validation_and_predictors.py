"""Run validation rules + predictors via `client.validation` / `client.predictors`.

Covers the workflow endpoints that `dhis2-core` mounts under
`dhis2 maintenance validation` / `dhis2 maintenance predictors`. CRUD on
the rules + predictors themselves stays on the generic `metadata` surface
(`dhis2 metadata list validationRules` etc.).

What the example exercises:

1. **Expression validation** — `/api/expressions/description` + per-context
   variants (`validation-rule`, `indicator`, `predictor`). Useful as a
   pre-save check before creating a VR or indicator: parses the formula
   + reports missing references.
2. **`run_analysis`** — `POST /api/dataAnalysis/validationRules`: evaluates
   every validation rule on the org-unit sub-tree for a date range and
   returns violations. Synchronous; no task polling.
3. **`list_results`** — browse DHIS2's persistent
   `/api/validationResults` table (populated by runs with `persist=True`).
4. **`predictors.run_all` / `run_group` / `run_one`** — triggers predictor
   engines that generate synthetic data values from historical data.

Usage:
    uv run python examples/client/validation_and_predictors.py
"""

from __future__ import annotations

from _runner import run_example
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env


async def main() -> None:
    """Run one of each — expression check, analysis, results list, predictors run."""
    async with open_client(profile_from_env()) as client:
        # 1. Expression validation — check two shapes: a valid DE ref + a bad one.
        print("--- expression validation ---")
        ok = await client.validation.describe_expression("#{fClA2Erf6IO}")
        print(f"  valid expression: {ok.valid} — description={ok.description!r}")

        bad = await client.validation.describe_expression("#{noSuchDeUid}")
        print(f"  invalid expression: {bad.valid} — message={bad.message!r}")

        # Per-context (validation-rule) — same DHIS2 parser as the VR engine uses.
        vr_ctx = await client.validation.describe_expression(
            "#{fClA2Erf6IO} > 0",
            context="validation-rule",
        )
        print(f"  VR-context: {vr_ctx.valid} — description={vr_ctx.description!r}")

        # 2. Run validation analysis (no rules on seeded instance, so 0 violations).
        print("\n--- validation analysis ---")
        violations = await client.validation.run_analysis(
            org_unit="ImspTQPwCqd",
            start_date="2025-01-01",
            end_date="2025-12-31",
        )
        print(f"  {len(violations)} violations on the seeded stack")
        for v in violations[:5]:
            print(
                f"    rule={v.validationRuleDescription or v.validationRuleId}  "
                f"pe={v.periodDisplayName or v.periodId}  "
                f"ou={v.organisationUnitDisplayName or v.organisationUnitId}  "
                f"left={v.leftSideValue} {v.operator} right={v.rightSideValue}"
            )

        # 3. Browse persisted results (empty unless some run had `persist=True`).
        print("\n--- persisted validation results ---")
        results = await client.validation.list_results(page_size=5)
        print(f"  {len(results)} persisted results")

        # 4. Run predictors (none seeded, so the engine just reports 0 predictions).
        print("\n--- predictors ---")
        envelope = await client.predictors.run_all(start_date="2025-01-01", end_date="2025-01-31")
        count = envelope.import_count()
        print(
            f"  status={envelope.status or envelope.httpStatus}  "
            f"imported={count.imported if count else '?'}  "
            f"message={envelope.message or '-'}"
        )


if __name__ == "__main__":
    run_example(main)
