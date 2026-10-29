"""Module 3 requirements: execution eligibility is separate from model advice."""
from copy import deepcopy

import pytest

from app.ai.gateway import LLMGateway
from app.ai.providers.mock import MockProvider
from app.exercises.execution import select_action
from app.workflows.process_claim import process_claim


def context(service, claim_id):
    return {key: getattr(service, method)(claim_id) for key, method in [
        ('claim', 'get_claim'), ('policy', 'get_policy'), ('evidence', 'get_evidence'),
        ('checks', 'calculate_policy_checks'), ('previous_outcomes', 'get_previous_outcomes'),
    ]}


async def advice(service, settings, claim_id):
    source = context(service, claim_id)
    assessment, _ = await LLMGateway(MockProvider(), settings).assess(source, 'course')
    return assessment, source


@pytest.mark.parametrize('claim_id,expected', [('CLM-001', 'accept'), ('CLM-002', 'reject'), ('CLM-003', 'review')])
async def test_action_selection(service, settings, claim_id, expected):
    assessment, source = await advice(service, settings, claim_id)
    original = deepcopy(source)
    saved = assessment.model_dump()
    assert select_action(assessment, source['checks'], source['policy'], source['evidence']) == expected
    assert source == original and assessment.model_dump() == saved
    assert service.detail(claim_id)['status'] == 'submitted'


@pytest.mark.parametrize('claim_id', ['CLM-001', 'CLM-002'])
async def test_confidence_and_questions(service, settings, claim_id):
    assessment, source = await advice(service, settings, claim_id)
    for update in [{'confidence': 0.8999}, {'unresolved_questions': ['Unverified detail']}, {'recommendation': 'investigate'}]:
        assert select_action(assessment.model_copy(update=update), source['checks'], source['policy'], source['evidence']) == 'review'
    assert select_action(assessment.model_copy(update={'confidence': 0.9, 'unresolved_questions': []}), source['checks'], source['policy'], source['evidence']) == ('accept' if claim_id == 'CLM-001' else 'reject')


async def test_policy_permissions(service, settings):
    for claim_id, permission in [('CLM-001', 'auto_accept'), ('CLM-002', 'auto_reject')]:
        assessment, source = await advice(service, settings, claim_id)
        source['policy'][permission] = False
        assert select_action(assessment, source['checks'], source['policy'], source['evidence']) == 'review'


async def test_evidence_coverage(service, settings):
    assessment, source = await advice(service, settings, 'CLM-001')
    for ids in [[], ['invented-receipt']]:
        assert select_action(assessment.model_copy(update={'evidence_ids': ids}), source['checks'], source['policy'], source['evidence']) == 'review'
    # Advice alone cannot turn the taxi's missing receipt into an eligible acceptance.
    assessment, source = await advice(service, settings, 'CLM-003')
    forced = assessment.model_copy(update={'recommendation': 'accept', 'confidence': 1.0, 'unresolved_questions': []})
    assert select_action(forced, source['checks'], source['policy'], source['evidence']) == 'review'


async def test_rejection_requires_cited_failure(service, settings):
    assessment, source = await advice(service, settings, 'CLM-002')
    assert any(c['severity'] == 'reject' for c in source['checks'])
    # A real rejection check must be among the codes cited by this advice.
    wrong = assessment.model_copy(update={'findings': ['unrelated-code']})
    assert select_action(wrong, source['checks'], source['policy'], source['evidence']) == 'review'
    assessment, source = await advice(service, settings, 'CLM-001')
    assert select_action(assessment.model_copy(update={'recommendation': 'reject'}), source['checks'], source['policy'], source['evidence']) == 'review'


@pytest.mark.parametrize('claim_id,status', [('CLM-001', 'accepted'), ('CLM-002', 'rejected'), ('CLM-003', 'pending_manager_review')])
async def test_workflow_outcomes(service, settings, claim_id, status):
    result = await process_claim(service, claim_id, 1, settings)
    assert result['status'] == status
    if status == 'pending_manager_review':
        assert result['review']['active'] and result['outcome'] is None
    else:
        assert result['review'] is None and result['outcome']['final_decision'] == status
    assert result['executions'][0]['status'] == 'succeeded'
    assert result['history']
