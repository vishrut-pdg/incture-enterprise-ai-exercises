# Module 2 debugging

## Processing fails in the untouched starter

Check: `./scripts/test-module2.sh` from the root. Cause: the learner boundary is intentionally incomplete. Fix: implement `TODO(MODULE2)` in `backend/app/exercises/recommendation.py`. Processing history records the original failure; the claim stays undecided.

## Validation says a source reference is unknown

Check supplied `checks[].code` and `evidence[].id`. Cause: the model or your code invented a reference. Fix: reject values outside those supplied sets, even when a reference sounds plausible. Empty evidence must stay empty.

## An unexpected decision appears

Check `Assessment` in `backend/app/schemas/assessment.py`. Only lowercase accept/reject are valid advice values; no assessment should finalize a claim. Fix: use strict Pydantic parsing and preserve manager review.

## Progressive hints

1. Which values are facts, and which are already-calculated findings?
2. Inspect `ClaimService.get_claim`, `get_policy`, `get_evidence`, and `calculate_policy_checks`.
3. `Assessment.model_validate_json` validates shape; you must also compare output reference sets against source IDs.

See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for startup, ports, queues, providers and stale UI.
