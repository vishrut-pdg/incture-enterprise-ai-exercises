# Module 3 — Execute with controls

## What you are building

Build the execution eligibility gate inside the complete application shown by the instructor. The business question is: **When may the application act on AI advice?** Your function chooses a result; ClaimService owns database writes, source/version checks and audit.

## What is already provided

- Completed retrieval, deterministic policy checks, strict model schemas and provider-neutral inference.
- React UI, seeded claims, migrations, repositories, manager controls appropriate to this module and read-only chat.
- ARQ worker, optional policy RAG, outcome memory, audit trail, and AI Usage & Performance dashboard.
- Reference tests, local infrastructure, mock provider and isolated module data/queue.

## What you need to implement

- Require confidence >= 0.90 and no unresolved questions before automatic execution.
- Allow acceptance only with policy permission, all checks passing, and complete evidence references.
- Allow rejection only with policy permission and a cited deterministic rejection finding.
- Return review for investigation advice, uncertainty, or any other ineligible case.

## Files you may edit

`backend/app/exercises/execution.py` only. Search `TODO(MODULE3)`. There are four TODOs in one function, `select_action`; expect roughly 20–40 meaningful lines.

## Files you should not edit

- `backend/app/domain/`, `backend/app/db/`, `backend/migrations/`, and `backend/app/seed.py`.
- `backend/app/assessment/`, `backend/app/agents/`, `backend/app/tools/`, `backend/app/ai/` and `backend/app/jobs/`.
- `backend/app/analytics/`, `backend/app/api/`, `backend/tests/`, unrelated frontend components and root Docker/scripts infrastructure.

## Start the application

Stop any other module first. From the repository root, in macOS/Linux Bash or [Ubuntu Bash on Windows WSL2](../WINDOWS.md):

```bash
bash scripts/setup-module3.sh
bash scripts/doctor.sh 3
bash scripts/start-module3.sh
```

## Run the exercise

Open http://localhost:5173. Read [EXERCISE.md](EXERCISE.md) and implement the four TODOs in the allowed file. Use Run in Claim queue to process seeded claims.

Browsing, grounded chat and usage infrastructure are provided. Successful processing depends on completing the TODOs. Module 3 includes completed earlier capabilities; copying code from earlier exercises is unnecessary.

## Validate

In another terminal, from the same repository root:

```bash
bash scripts/test-module3.sh
```

## Success looks like

CLM-001 is accepted, CLM-002 rejected, and CLM-003 sent to manager review. Validation ends with `MODULE 3 EXERCISE PASSED`.

## Stuck?

Read [DEBUGGING.md](DEBUGGING.md) and [root troubleshooting](../TROUBLESHOOTING.md). Reset application data with `bash scripts/reset-module3.sh` after stopping the application; learner source is preserved.
