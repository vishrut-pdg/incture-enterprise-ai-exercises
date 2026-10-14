# Module 2 exercise

## GOAL

Build a structured recommendation for manager review with roughly 20–40 meaningful lines in one file.

## BUSINESS SCENARIO

CLM-001 is a compliant client lunch; CLM-002 is disallowed personal entertainment; CLM-003 lacks a receipt. Produce grounded advice and leave the final decision to the manager.

## ARCHITECTURE CONTEXT

ClaimTools already retrieves serialized source facts and deterministic checks through ClaimService. LLMGateway already handles provider calls, request schemas, timeout, logging and usage. You implement only the small boundary in `backend/app/exercises/recommendation.py`.

## YOUR TASK

- Parse the strict Assessment schema (accept/reject only, confidence 0–1, required fields).
- Reject finding codes absent from supplied checks.
- Reject unknown evidence IDs and return validated advice without writing business state.

## FILES TO EDIT

`backend/app/exercises/recommendation.py` only. Search `TODO(MODULE2)`.

## TODO 1

Parse the strict Assessment schema (accept/reject only, confidence 0–1, required fields).

## TODO 2

Reject finding codes absent from supplied checks.

## TODO 3

Reject unknown evidence IDs and return validated advice without writing business state.


The source context has `claim`, `policy`, `evidence`, `checks`, and `previous_outcomes`. Finding identifiers live in `checks[].code`; evidence identifiers live in `evidence[].id`. An empty evidence list is valid. The wire field is `findings`; Module 2 recommendation values are lowercase `accept` and `reject`. Preserve the reference schema rather than accepting alternate spellings. For unknown references raise `ValueError("Assessment contains unknown references")` to preserve the reference diagnostic; Pydantic ValidationError already subclasses ValueError.

## DO NOT CHANGE

Policy rules, schema, database, seed data, provider adapters, manager actions, logging, Docker, tests or unrelated UI. Do not create evidence. Do not finalize a claim from AI output.

## HOW TO RUN

From the repository root: `./scripts/setup-module2.sh`, then `./scripts/start-module2.sh`. Use a second terminal for validation.

## HOW TO TEST

`./scripts/test-module2.sh` reports each requirement with a focused hint. A red starter result is intentional. After success, run the retained reference tests for broader confidence (see CONTRIBUTING.md).

## EXPECTED RESULT

Known grounded advice is accepted. Unknown sources and arbitrary recommendation values are rejected. All processed claims have an active manager review and no final outcome.

## OPTIONAL CHALLENGE

After validation passes, enable optional mock policy retrieval as described in COURSE_GUIDE.md and inspect its source passages and usage telemetry. Keep deterministic checks authoritative.
