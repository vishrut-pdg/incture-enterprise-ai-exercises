# Module 4 — Investigate and decide autonomously

## What you are building

Resolve a grounded autonomous decision inside the complete application shown by the instructor. The business question is: **Can a bounded workflow resolve a claim without a Run click or manager approval?** Your function chooses a result; ClaimService owns database writes, source/version checks and audit.

## What is already provided

- Completed retrieval, deterministic policy checks, strict model schemas and provider-neutral inference.
- React UI, seeded claims, migrations, repositories, manager controls appropriate to this module and read-only chat.
- ARQ worker, optional policy RAG, outcome memory, audit trail, and AI Usage & Performance dashboard.
- Reference tests, local infrastructure, mock provider and isolated module data/queue.

## What you need to implement

- Gather non-pass check messages, investigation limitations, unresolved questions and confidence gaps.
- Accept only when both stages support accept at confidence >= 0.90, both cite all evidence, all checks pass and policy permits acceptance.
- Otherwise reject under the supplied course policy; raise ValueError when policy disables automatic rejection.
- Return a new assessment with a binary decision and an explanation; clear decision questions without mutating source inputs.

## Files you may edit

`backend/app/exercises/autonomy.py` only. Search `TODO(MODULE4)`. There are four TODOs in one function, `resolve_assessment`; expect roughly 20–40 meaningful lines.

## Files you should not edit

- `backend/app/domain/`, `backend/app/db/`, `backend/migrations/`, and `backend/app/seed.py`.
- `backend/app/assessment/`, `backend/app/agents/`, `backend/app/tools/`, `backend/app/ai/` and `backend/app/jobs/`.
- `backend/app/analytics/`, `backend/app/api/`, `backend/tests/`, unrelated frontend components and root Docker/scripts infrastructure.

## Start the application

Stop any other module first. From the repository root, in macOS/Linux Bash or [Ubuntu Bash on Windows WSL2](../WINDOWS.md):

```bash
bash scripts/setup-module4.sh
bash scripts/doctor.sh 4
bash scripts/start-module4.sh
```

## Run the exercise

Open http://localhost:5173. Read [EXERCISE.md](EXERCISE.md) and implement the four TODOs in the allowed file. The worker starts discovery immediately and repeats every five seconds. There is no Run or approval step. In the untouched starter, processing records failures safely and retries after cooldown. Stop/restart after editing; reset data if needed to remove stale retry results.

Browsing, grounded chat and usage infrastructure are provided. Successful processing depends on completing the TODOs. Module 4 includes completed earlier capabilities; copying code from earlier exercises is unnecessary.

## Validate

In another terminal, from the same repository root:

```bash
bash scripts/test-module4.sh
```

## Success looks like

The worker discovers claims automatically. CLM-001 is accepted; CLM-002 and CLM-003 are rejected after investigation. No manager review is created. Validation ends with `MODULE 4 EXERCISE PASSED`.

## Stuck?

Read [DEBUGGING.md](DEBUGGING.md) and [root troubleshooting](../TROUBLESHOOTING.md). Reset application data with `bash scripts/reset-module4.sh` after stopping the application; learner source is preserved.
