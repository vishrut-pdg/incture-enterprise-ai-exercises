"""Validate structured manager advice; called by the metered LLM gateway.

Grounded retrieval is complete in this starter. Return a validated Assessment.
Never write claims, invoke providers, or finalize a manager decision here.
"""
from app.schemas.assessment import Assessment

# ============================================================
# LEARNER TODO — MODULE 2
# Goal: structured recommendation grounded in known findings/evidence.
# Accept/Reject is advice. The manager owns the final decision.
# Validate: ./scripts/test-module2.sh
# ============================================================


def validate_recommendation(content: str, context: dict) -> Assessment:
    """Return strict validated advice or raise ValueError for invalid output."""
    # TODO(MODULE2): Parse JSON using Assessment.model_validate_json (strict schema).
    # TODO(MODULE2): Reject finding codes absent from context["checks"].
    # TODO(MODULE2): Reject evidence IDs absent from context["evidence"], then return assessment.
    # WHY: Provider text is untrusted until both shape and source references are checked.
    raise ValueError("Module 2 exercise incomplete: implement validate_recommendation in app/exercises/recommendation.py")
