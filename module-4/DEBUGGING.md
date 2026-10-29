# Module 4 debugging

## Starter processing records failures

Symptom: the UI opens but processing does not produce expected outcomes. Check: `bash scripts/test-module4.sh` and claim processing history. Cause: the learner function intentionally raises an exercise-incomplete error. Fix: implement `TODO(MODULE4)` in `backend/app/exercises/autonomy.py`. Do not bypass the function or loosen real tests.

## An action has the wrong owner

Check the three hero claims and compare their findings, policy flags and model advice. Fix: follow EXERCISE.md's eligibility rules. CLM-003 must be rejected under the supplied autonomous receipt policy, with an investigation and explanation. No manager review is added in autonomous mode.

## Progressive hints

1. Separate current deterministic findings from advice, and list every prerequisite for acceptance.
2. Compare evidence ID sets against the supplied evidence list; a plausible model ID is not proof of a record.
3. Inspect the existing Assessment contract and provided ClaimService wrapper. Select/return a result; let that service persist it.

## Claim remains submitted after editing

Check execution history and worker logs. Cause: a technical failure or a cached failed autonomous job can be waiting for cooldown (300 seconds by default). Fix: stop all module processes, run `bash scripts/reset-module4.sh`, then restart. Reset clears only this module's stable autonomous job namespace and restores seed data, preserving learner source. Never turn an outage into a business rejection.

## A provider outage appears as rejection

Cause: exception handling was moved into the decision function. Fix: remove that handling; the provided workflow records failures, keeps the claim undecided and lets the worker retry. Only validated inputs reach the learner rule.

See [root troubleshooting](../TROUBLESHOOTING.md) for ports, worker, database, provider and stale UI issues.
