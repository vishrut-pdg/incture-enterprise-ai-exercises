"""Build grounded context and validate a factual summary. Called by agent/gateway.

Source records and deterministic findings are already retrieved for you.
This module does not own policy calculation, evidence creation or business decisions.
"""
from app.schemas.assessment import Assessment

# ============================================================
# LEARNER TODO — MODULE 1
# Goal: facts + policy + evidence + supplied checks -> grounded summary.
# Do not create evidence, recalculate policy or recommend Accept/Reject.
# Validate: ./scripts/test-module1.sh
# ============================================================


def build_context(source: dict) -> dict:
    """Return an independent JSON-compatible context from the retrieved source."""
    # TODO(MODULE1): Copy claim and policy into a new context without mutating source.
    # TODO(MODULE1): Include evidence and checks exactly as supplied, including empty evidence.
    # TODO(MODULE1): Preserve previous_outcomes and any optional policy_passages.
    raise ValueError("Module 1 exercise incomplete: implement build_context in app/exercises/summary.py")


def validate_summary(content: str, context: dict) -> Assessment:
    """Parse strict facts-only output and reject references outside source context."""
    # TODO(MODULE1): Parse with Assessment.model_validate_json; reject unknown evidence/findings.
    # WHY: A plausible model reference is not proof that a source record exists.
    raise ValueError("Module 1 exercise incomplete: implement validate_summary in app/exercises/summary.py")
