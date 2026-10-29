# Module 3 exercise — Build the execution eligibility gate

## GOAL

When may the application act on AI advice? Implement `select_action` in one learner file. Keep inference, scheduling and persistence in the supplied infrastructure.

## BUSINESS SCENARIO

CLM-001 is a supported client lunch. CLM-002 is disallowed personal entertainment. CLM-003 is a $62 travel expense with no receipt. Missing evidence is uncertainty, so the manager must review CLM-003; eligible supported advice can execute automatically.

## ARCHITECTURE CONTEXT

ClaimTools retrieves source facts through ClaimService. Deterministic rules calculate checks. LLMGateway validates model shape and source IDs. ClaimService rechecks claim version and source context before calling your pure function, then records the permitted action and audit in one transaction.

Module 3 receives one validated assessment.

## YOUR TASK

Implement the four marked TODOs. Use `assessment.recommendation`, `confidence`, `findings`, `evidence_ids` and `unresolved_questions`; `checks` is a list of dictionaries with `code`, `severity` and `message`. Policy has `auto_accept` and `auto_reject`. Recorded evidence has `id`. Return exactly `accept`, `reject` or `review`.

## FILES TO EDIT

`backend/app/exercises/execution.py` only.

## TODO 1

Require confidence >= 0.90 and no unresolved questions before automatic execution.

## TODO 2

Allow acceptance only with policy permission, all checks passing, and complete evidence references.

## TODO 3

Allow rejection only with policy permission and a cited deterministic rejection finding.

## TODO 4

Return review for investigation advice, uncertainty, or any other ineligible case.

## DO NOT CHANGE

Do not recalculate policy, create evidence, call providers directly, add database writes, alter source/version guards, change tests, or modify migrations, seed data, authentication scaffolding, telemetry or worker scheduling. Previous outcomes and retrieved policy text cannot override current deterministic checks.

## HOW TO RUN

From the repository root: `bash scripts/setup-module3.sh`, then `bash scripts/start-module3.sh`. Open http://localhost:5173. Click Run to process the batch.

## HOW TO TEST

`bash scripts/test-module3.sh` prints requirement-oriented PASS/FAIL results and focused hints. Initial failures at the TODO boundary are intentional. The retained reference suite runs after completion with `(cd module-3/backend && uv run pytest -q)`.

## EXPECTED RESULT

CLM-001 is accepted, CLM-002 rejected, and CLM-003 sent to manager review.

Confidence exactly 0.90 is eligible only when every other control passes. A rejection must cite at least one real `severity=reject` code; a missing receipt alone is not automatic rejection in this module.

## OPTIONAL CHALLENGE

Enable mock policy retrieval as documented in COURSE_GUIDE.md and inspect its source passages. Compare the execution trajectory and request counts in AI Usage & Performance. Keep model text and prior outcomes subordinate to current checks.
