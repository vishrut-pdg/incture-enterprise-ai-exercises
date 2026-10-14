# Module 1

## What you are building

Build a grounded factual summary inside the same application shown by the instructor. AI must not recommend Accept/Reject.

## What is already provided

- React UI, API, database, migrations and seeded claims.
- Policy checks, evidence retrieval, repositories and bounded agents.
- Provider adapters, gateway, manager review, audit and AI Usage & Performance dashboard.
- Local worker, reference tests and optional RAG.

## What you need to implement

- Copy claim and policy into an independent JSON-compatible context.
- Include recorded evidence and supplied deterministic checks unchanged.
- Preserve prior outcomes and optional policy passages.
- Parse strict factual output; reject unknown finding codes and evidence IDs.

## Files you may edit

`backend/app/exercises/summary.py` — the only learner code file.

## Files you should not edit

- `backend/app/domain/`, `backend/app/db/`, `backend/migrations/` and `backend/app/seed.py`.
- `backend/app/ai/`, `backend/app/analytics/`, `backend/app/telemetry/` and `backend/app/jobs/`.
- `backend/app/api/`, `backend/app/assessment/`, `backend/app/agents/` and `backend/app/tools/`.
- `backend/tests/`, unrelated frontend files and root Docker/scripts infrastructure.

## Start the application

From the repository root:

```bash
./scripts/setup-module1.sh
./scripts/start-module1.sh
```

## Run the exercise

Open http://localhost:5173. Read [EXERCISE.md](EXERCISE.md), implement `TODO(MODULE1)` in the allowed file, then retry processing. The starter displays claims and allows browsing, chat and usage inspection; processing fails safely until the task is complete. No business decision is made on failure.

## Validate

```bash
./scripts/test-module1.sh
```

## Success looks like

CLM-003 shows the $62 travel claim and missing receipt finding, with no AI recommendation. It awaits a human decision.

Validation ends with `MODULE 1 EXERCISE PASSED`.

## Stuck?

Read [DEBUGGING.md](DEBUGGING.md) and [root troubleshooting](../TROUBLESHOOTING.md).
