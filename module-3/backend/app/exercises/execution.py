"""Choose a controlled action from validated advice and current deterministic facts.

Called by ClaimService after source/version revalidation. Return an action string;
do not write records, invoke providers or calculate policy rules here.
"""
from typing import Literal

from app.schemas.assessment import Assessment

# ============================================================
# LEARNER TODO — MODULE 3
# Goal: eligible advice -> controlled execution; uncertainty -> review.
# Only edit this file. Validate: bash scripts/test-module3.sh
# ============================================================


def select_action(assessment: Assessment, checks: list[dict], policy: dict,
                  evidence: list[dict]) -> Literal["accept", "reject", "review"]:
    """Select an action without mutating assessment, source data or business state."""
    # TODO(MODULE3): Require confidence >= 0.90 and no unresolved questions for automation.
    # TODO(MODULE3): Accept only if policy permits, every check passes and all evidence is cited.
    # TODO(MODULE3): Reject only if policy permits and advice cites a deterministic rejection code.
    # TODO(MODULE3): Send investigate, uncertainty and every ineligible case to manager review.
    raise ValueError("Module 3 exercise incomplete: implement select_action in app/exercises/execution.py")
