# Module 1 exercise

## GOAL

Build a grounded factual summary with roughly 20–40 meaningful lines in one file.

## BUSINESS SCENARIO

CLM-003 is a $62 taxi claim. Travel is allowed, the amount is within policy, and the receipt is missing. Report those facts without inventing evidence or recommending a decision.

## ARCHITECTURE CONTEXT

ClaimTools already retrieves serialized source facts and deterministic checks through ClaimService. LLMGateway already handles provider calls, request schemas, timeout, logging and usage. You implement only the small boundary in `backend/app/exercises/summary.py`.

## YOUR TASK

- Copy claim and policy into an independent JSON-compatible context.
- Include recorded evidence and supplied deterministic checks unchanged.
- Preserve prior outcomes and optional policy passages.
- Parse strict factual output; reject unknown finding codes and evidence IDs.

## FILES TO EDIT

`backend/app/exercises/summary.py` only. Search `TODO(MODULE1)`.

## TODO 1

Copy claim and policy into an independent JSON-compatible context.

## TODO 2

Include recorded evidence and supplied deterministic checks unchanged.

## TODO 3

Preserve prior outcomes and optional policy passages.

## TODO 4

Parse strict factual output; reject unknown finding codes and evidence IDs.


The source context has `claim`, `policy`, `evidence`, `checks`, and `previous_outcomes`. Finding identifiers live in `checks[].code`; evidence identifiers live in `evidence[].id`. An empty evidence list is valid. The wire field is `findings`; Module 2 recommendation values are lowercase `accept` and `reject`. Preserve the reference schema rather than accepting alternate spellings. For unknown references raise `ValueError("Assessment contains unknown references")` to preserve the reference diagnostic; Pydantic ValidationError already subclasses ValueError.

## DO NOT CHANGE

Policy rules, schema, database, seed data, provider adapters, manager actions, logging, Docker, tests or unrelated UI. Do not create evidence. Do not finalize a claim from AI output.

## HOW TO RUN

From the repository root: `./scripts/setup-module1.sh`, then `./scripts/start-module1.sh`. Use a second terminal for validation.

## HOW TO TEST

`./scripts/test-module1.sh` reports each requirement with a focused hint. A red starter result is intentional. After success, run the retained reference tests for broader confidence (see CONTRIBUTING.md).

## EXPECTED RESULT

CLM-003 remains manager-owned. Its summary includes known checks, no evidence IDs and no recommendation field.

## OPTIONAL CHALLENGE

After validation passes, enable optional mock policy retrieval as described in COURSE_GUIDE.md and inspect its source passages and usage telemetry. Keep deterministic checks authoritative.
