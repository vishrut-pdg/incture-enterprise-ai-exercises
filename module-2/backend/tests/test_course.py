"""Validate learner recommendation boundary and preserve manager authority."""
import json

import pytest

from app.ai.models import LLMRequest
from app.ai.providers.mock import MockProvider
from app.exercises.recommendation import validate_recommendation
from app.workflows.process_claim import process_claim


def source(service, claim_id='CLM-001'):
    return {key: getattr(service, method)(claim_id) for key, method in [
        ('claim', 'get_claim'), ('policy', 'get_policy'), ('evidence', 'get_evidence'),
        ('checks', 'calculate_policy_checks'), ('previous_outcomes', 'get_previous_outcomes'),
    ]}


async def output(context):
    return (await MockProvider().generate(LLMRequest(
        model='mock', system='', context=context, response_schema={}, correlation_id='course'
    ))).content


async def test_structured_advice(service):
    context = source(service)
    assessment = validate_recommendation(await output(context), context)
    assert assessment.recommendation == 'accept'
    assert assessment.explanation and assessment.findings
    assert assessment.evidence_ids == ['CLM-001-receipt']
    assert 0 <= assessment.confidence <= 1


@pytest.mark.parametrize('claim_id,expected', [('CLM-001','accept'),('CLM-002','reject'),('CLM-003','reject')])
async def test_hero_cases(service, settings, claim_id, expected):
    result = await process_claim(service, claim_id, 1, settings)
    assert result['assessment']['data']['recommendation'] == expected
    assert result['status'] == 'pending_manager_review'
    assert result['review']['active']
    assert result['outcome'] is None


async def test_unknown_findings(service):
    context = source(service)
    content = json.loads(await output(context))
    assert validate_recommendation(json.dumps(content), context).recommendation == 'accept'
    with pytest.raises(ValueError):
        validate_recommendation(json.dumps(dict(content, findings=['invented'])), context)


async def test_unknown_evidence(service):
    for claim in ['CLM-001', 'CLM-003']:
        context = source(service, claim)
        content = json.loads(await output(context))
        assert validate_recommendation(json.dumps(content), context).explanation
        with pytest.raises(ValueError):
            validate_recommendation(json.dumps(dict(content, evidence_ids=['invented'])), context)


async def test_invalid_contract(service):
    context = source(service)
    content = json.loads(await output(context))
    assert validate_recommendation(json.dumps(content), context).recommendation == 'accept'
    for field, value in [('recommendation','investigate'),('recommendation','Accept'),('confidence',1.2),('confidence','0.9'),('findings',[]),('explanation','')]:
        with pytest.raises(ValueError):
            validate_recommendation(json.dumps(dict(content, **{field:value})), context)
    incomplete = dict(content)
    del incomplete['unresolved_questions']
    with pytest.raises(ValueError):
        validate_recommendation(json.dumps(incomplete), context)
    with pytest.raises(ValueError):
        validate_recommendation(json.dumps(dict(content, final_decision='accepted')), context)
