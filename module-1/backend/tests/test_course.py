"""Exercise requirements tested directly and through the real application workflow."""
import json
from copy import deepcopy

import pytest

from app.ai.models import LLMRequest
from app.ai.providers.mock import MockProvider
from app.exercises.summary import build_context, validate_summary
from app.workflows.process_claim import process_claim


def source(service, claim_id='CLM-003'):
    return {key: getattr(service, method)(claim_id) for key, method in [
        ('claim', 'get_claim'), ('policy', 'get_policy'), ('evidence', 'get_evidence'),
        ('checks', 'calculate_policy_checks'), ('previous_outcomes', 'get_previous_outcomes'),
    ]}


async def output(context):
    return (await MockProvider().generate(LLMRequest(
        model='mock', system='', context=context, response_schema={}, correlation_id='course'
    ))).content


def test_claim_and_policy(service):
    original = source(service)
    saved = deepcopy(original)
    context = build_context(original)
    assert context['claim'] == saved['claim']
    assert context['policy'] == saved['policy']
    assert original == saved
    context['claim']['title'] = 'changed'
    context['policy']['name'] = 'changed'
    assert original == saved, 'Context must not share mutable source objects'


def test_missing_receipt_and_evidence(service):
    original = source(service)
    context = build_context(original)
    assert context['evidence'] == []
    assert context['checks'] == original['checks']
    assert any(c['code'] == 'receipt_required' and c['severity'] == 'unverified' for c in context['checks'])
    assert context['previous_outcomes'] == original['previous_outcomes']


def test_optional_passages(service):
    original = source(service)
    original['policy_passages'] = [{'id': 'policy:1', 'content': 'Receipt required'}]
    saved = deepcopy(original)
    context = build_context(original)
    assert context['policy_passages'] == original['policy_passages']
    context['policy_passages'][0]['content'] = 'changed'
    assert original == saved


async def test_valid_factual_output(service):
    context = source(service, 'CLM-001')
    assessment = validate_summary(await output(context), context)
    assert assessment.summary
    assert assessment.evidence_ids == ['CLM-001-receipt']
    assert set(assessment.findings) <= {c['code'] for c in context['checks']}
    assert 'recommendation' not in assessment.model_dump()


async def test_unknown_references(service):
    context = source(service)
    content = json.loads(await output(context))
    for field, value in [('evidence_ids', ['invented-receipt']), ('findings', ['invented-finding'])]:
        invalid = dict(content, **{field: value})
        with pytest.raises(ValueError):
            validate_summary(json.dumps(invalid), context)
    # Prevent a stub that rejects everything from passing the negative checks.
    assert validate_summary(json.dumps(content), context).evidence_ids == []


async def test_no_recommendation(service):
    context = source(service)
    content = json.loads(await output(context))
    assert validate_summary(json.dumps(content), context).summary
    for value in ['accept', 'reject', 'investigate']:
        with pytest.raises(ValueError):
            validate_summary(json.dumps(dict(content, recommendation=value)), context)
    with pytest.raises(ValueError):
        validate_summary(json.dumps(dict(content, confidence=1.2)), context)


async def test_human_owns_claim(service, settings):
    result = await process_claim(service, 'CLM-003', 1, settings)
    assert result['status'] == 'pending_manager_review'
    assert result['review']['active']
    assert result['outcome'] is None
    assert 'recommendation' not in result['assessment']['data']
    assert result['assessment']['data']['evidence_ids'] == []
