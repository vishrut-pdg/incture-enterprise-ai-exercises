# Module 2

## What you are building

Build a structured recommendation for manager review inside the same application shown by the instructor. AI may recommend Accept/Reject; the manager owns the final action.

## What is already provided

- React UI, API, database, migrations and seeded claims.
- Policy checks, evidence retrieval, repositories and bounded agents.
- Provider adapters, gateway, manager review, audit and AI Usage & Performance dashboard.
- Local worker, reference tests and optional RAG.

## What you need to implement

- Parse the strict Assessment schema (accept/reject only, confidence 0–1, required fields).
- Reject finding codes absent from supplied checks.
- Reject unknown evidence IDs and return validated advice without writing business state.

## Files you may edit

`backend/app/exercises/recommendation.py` — the only learner code file.

## Files you should not edit

- `backend/app/domain/`, `backend/app/db/`, `backend/migrations/` and `backend/app/seed.py`.
- `backend/app/ai/`, `backend/app/analytics/`, `backend/app/telemetry/` and `backend/app/jobs/`.
- `backend/app/api/`, `backend/app/assessment/`, `backend/app/agents/` and `backend/app/tools/`.
- `backend/tests/`, unrelated frontend files and root Docker/scripts infrastructure.

## Start the application

From the repository root. **Windows:** first follow [Windows Bash setup](../WINDOWS.md), then run these commands in Ubuntu on WSL2:

```bash
bash scripts/setup-module2.sh
bash scripts/start-module2.sh
```

## Run the exercise

Open http://localhost:5173. Read [EXERCISE.md](EXERCISE.md), implement `TODO(MODULE2)` in the allowed file, then retry processing. The starter displays claims and allows browsing, chat and usage inspection; processing fails safely until the task is complete. No business decision is made on failure.

## Validate

```bash
bash scripts/test-module2.sh
```

## Success looks like

CLM-001 recommends Accept; CLM-002 and CLM-003 recommend Reject. Each still awaits manager review.

Validation ends with `MODULE 2 EXERCISE PASSED`.

## Stuck?

Read [DEBUGGING.md](DEBUGGING.md) and [root troubleshooting](../TROUBLESHOOTING.md).
