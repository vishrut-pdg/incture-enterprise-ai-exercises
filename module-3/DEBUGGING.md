# Module 3 debugging

## Starter processing records failures

Symptom: the UI opens but processing does not produce expected outcomes. Check: `bash scripts/test-module3.sh` and claim processing history. Cause: the learner function intentionally raises an exercise-incomplete error. Fix: implement `TODO(MODULE3)` in `backend/app/exercises/execution.py`. Do not bypass the function or loosen real tests.

## An action has the wrong owner

Check the three hero claims and compare their findings, policy flags and model advice. Fix: follow EXERCISE.md's eligibility rules. CLM-003 must remain manager-owned; a model cannot prove that its missing receipt exists.

## Progressive hints

1. Separate current deterministic findings from advice, and list every prerequisite for acceptance.
2. Compare evidence ID sets against the supplied evidence list; a plausible model ID is not proof of a record.
3. Inspect the existing Assessment contract and provided ClaimService wrapper. Select/return a result; let that service persist it.

See [root troubleshooting](../TROUBLESHOOTING.md) for ports, worker, database, provider and stale UI issues.
