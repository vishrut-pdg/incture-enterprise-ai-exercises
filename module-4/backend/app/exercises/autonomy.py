"""Resolve two validated model stages into a bounded autonomous decision.

ClaimService calls this after validating investigation sources and claim version.
This pure function owns the decision rule, never persistence, scheduling or inference.
The supplied course policy rejects unmet requirements; technical failures stay undecided.
"""
from app.schemas.assessment import Assessment, Investigation

# ============================================================
# LEARNER TODO — MODULE 4
# Goal: grounded investigation + assessment -> binary autonomous outcome.
# Only edit this file. Validate: bash scripts/test-module4.sh
# ============================================================


def resolve_assessment(assessment: Assessment, investigation: Investigation,
                       checks: list[dict], policy: dict,
                       evidence: list[dict]) -> Assessment:
    """Return a new assessment with a policy-supported binary decision and explanation."""
    # TODO(MODULE4): Gather non-pass check messages, limitations, questions and low-confidence reasons.
    # TODO(MODULE4): Accept only if BOTH stages support accept, confidence >= 0.90,
    #                all evidence is cited by BOTH stages, all checks pass and policy permits it.
    # TODO(MODULE4): Otherwise reject under course policy; raise ValueError if auto_reject is disabled.
    # TODO(MODULE4): Return a new assessment, explaining rejection reasons and clearing resolved
    #                decision questions. Never mutate the inputs or create manager review.
    raise ValueError("Module 4 exercise incomplete: implement resolve_assessment in app/exercises/autonomy.py")
