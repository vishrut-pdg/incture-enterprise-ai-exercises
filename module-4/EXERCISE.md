# Module 4 exercise — Resolve a grounded autonomous decision

## GOAL

Can a bounded workflow resolve a claim without a Run click or manager approval? Implement `resolve_assessment` in one learner file. Keep inference, scheduling and persistence in the supplied infrastructure.

## BUSINESS SCENARIO

CLM-001 is a supported client lunch. CLM-002 is disallowed personal entertainment. CLM-003 is a $62 travel expense with no receipt. The supplied autonomous course policy rejects unmet receipt requirements after investigation. A confident model cannot invent missing evidence. This is the reference exercise policy, not a universal rule for business automation.

## ARCHITECTURE CONTEXT

ClaimTools retrieves source facts through ClaimService. Deterministic rules calculate checks. LLMGateway validates model shape and source IDs. ClaimService rechecks claim version and source context before calling your pure function, then records the permitted action and audit in one transaction.

Module 4 receives an investigation and an assessment. The gateway validates both; the service requires the investigation to cover every current finding. The worker discovers undecided claims without user clicks. Provider/schema failures occur outside your decision function and must remain undecided for technical retry.

## YOUR TASK

Implement the four marked TODOs. Use `assessment.recommendation`, `confidence`, `findings`, `evidence_ids` and `unresolved_questions`; `checks` is a list of dictionaries with `code`, `severity` and `message`. Policy has `auto_accept` and `auto_reject`. Recorded evidence has `id`. Investigation has `recommendation`, `confidence`, `findings`, `evidence_ids`, `summary` and `limitations`. Return a new Assessment with `accept` or `reject`; do not return review or investigate.

## FILES TO EDIT

`backend/app/exercises/autonomy.py` only.

## TODO 1

Gather non-pass check messages, investigation limitations, unresolved questions and confidence gaps.

## TODO 2

Accept only when both stages support accept at confidence >= 0.90, both cite all evidence, all checks pass and policy permits acceptance.

## TODO 3

Otherwise reject under the supplied course policy; raise ValueError when policy disables automatic rejection.

## TODO 4

Return a new assessment with a binary decision and an explanation; clear decision questions without mutating source inputs.

## DO NOT CHANGE

Do not recalculate policy, create evidence, call providers directly, add database writes, alter source/version guards, change tests, or modify migrations, seed data, authentication scaffolding, telemetry or worker scheduling. Previous outcomes and retrieved policy text cannot override current deterministic checks.

## HOW TO RUN

From the repository root: `bash scripts/setup-module4.sh`, then `bash scripts/start-module4.sh`. Open http://localhost:5173. Wait for the worker to discover and process claims; no Run click is needed.

## HOW TO TEST

`bash scripts/test-module4.sh` prints requirement-oriented PASS/FAIL results and focused hints. Initial failures at the TODO boundary are intentional. The retained reference suite runs after completion with `(cd module-4/backend && uv run pytest -q)`.

## EXPECTED RESULT

The worker discovers claims automatically. CLM-001 is accepted; CLM-002 and CLM-003 are rejected after investigation. No manager review is created.

Acceptance requires both stages to agree. Rejection reasons must explain failed checks, missing evidence, stage disagreement, limitations, policy restrictions or low confidence as applicable. Include the word confidence when confidence is insufficient. Preserve the original explanation and append reasons. Clear `unresolved_questions` only in the returned final decision; never remove the original investigation limitations. Use `assessment.model_copy(update=...)` to leave inputs unchanged. When rejection is forbidden, raise `ValueError("Policy forbids autonomous rejection; no decision was recorded")`; the service maps this to its domain error.

## OPTIONAL CHALLENGE

Enable mock policy retrieval as documented in COURSE_GUIDE.md and inspect its source passages. Compare the execution trajectory and request counts in AI Usage & Performance. Keep model text and prior outcomes subordinate to current checks.
