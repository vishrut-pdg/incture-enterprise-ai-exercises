"""Module 4 requirements: investigated facts bound autonomous decisions."""
import json
from copy import deepcopy

import pytest

from app.ai.gateway import LLMGateway
from app.ai.providers.mock import MockProvider
from app.assessment.service import DomainError
from app.exercises.autonomy import resolve_assessment
from app.workflows.process_claim import process_claim


async def stages(service, settings, claim_id='CLM-001'):
    settings.decision_mode = 'autonomous'
    source = {key: getattr(service, method)(claim_id) for key, method in [
        ('claim', 'get_claim'), ('policy', 'get_policy'), ('evidence', 'get_evidence'),
        ('checks', 'calculate_policy_checks'), ('previous_outcomes', 'get_previous_outcomes'),
    ]}
    gateway = LLMGateway(MockProvider(), settings)
    investigation, _ = await gateway.investigate(source, 'course')
    source['investigation'] = investigation.model_dump()
    assessment, _ = await gateway.assess(source, 'course')
    return assessment, investigation, source


def resolve(assessment, investigation, source):
    return resolve_assessment(assessment, investigation, source['checks'], source['policy'], source['evidence'])


async def test_supported_acceptance(service, settings):
    assessment, investigation, source = await stages(service, settings)
    original = deepcopy(source)
    before = (assessment.model_dump(), investigation.model_dump())
    result = resolve(assessment, investigation, source)
    assert result.recommendation == 'accept' and result.unresolved_questions == []
    assert result is not assessment
    assert source == original and (assessment.model_dump(), investigation.model_dump()) == before
    assert service.detail('CLM-001')['outcome'] is None


async def test_missing_receipt_cannot_be_invented(service, settings):
    assessment, investigation, source = await stages(service, settings, 'CLM-003')
    # Even mutually confident model text cannot overrule a failed deterministic requirement.
    assessment = assessment.model_copy(update={'recommendation': 'accept', 'unresolved_questions': [], 'confidence': 1.0})
    investigation = investigation.model_copy(update={'recommendation': 'accept', 'limitations': [], 'confidence': 1.0})
    result = resolve(assessment, investigation, source)
    assert result.recommendation == 'reject'
    assert 'receipt' in result.explanation.lower()
    assert result.evidence_ids == [] and result.unresolved_questions == []


async def test_uncertainty_and_disagreement(service, settings):
    assessment, investigation, source = await stages(service, settings)
    for update in [{'confidence': 0.8999}, {'limitations': ['Evidence could not be fully verified']}, {'recommendation': 'reject'}]:
        result = resolve(assessment, investigation.model_copy(update=update), source)
        assert result.recommendation == 'reject' and result.explanation != assessment.explanation
    for update in [{'confidence': 0.2}, {'unresolved_questions': ['Unknown detail']}, {'recommendation': 'reject'}]:
        assert resolve(assessment.model_copy(update=update), investigation, source).recommendation == 'reject'
    assert resolve(assessment.model_copy(update={'confidence': 0.9}), investigation.model_copy(update={'confidence': 0.9}), source).recommendation == 'accept'


async def test_evidence_coverage_and_policy(service, settings):
    assessment, investigation, source = await stages(service, settings)
    assert resolve(assessment.model_copy(update={'evidence_ids': []}), investigation, source).recommendation == 'reject'
    assert resolve(assessment, investigation.model_copy(update={'evidence_ids': []}), source).recommendation == 'reject'
    source['policy']['auto_accept'] = False
    assert resolve(assessment, investigation, source).recommendation == 'reject'
    source['policy']['auto_reject'] = False
    with pytest.raises(ValueError):
        resolve(assessment, investigation, source)


@pytest.mark.parametrize('claim_id,status', [('CLM-001', 'accepted'), ('CLM-002', 'rejected'), ('CLM-003', 'rejected')])
async def test_autonomous_outcomes_and_audit(service, settings, claim_id, status):
    settings.decision_mode = 'autonomous'
    result = await process_claim(service, claim_id, 1, settings)
    assert result['status'] == status and result['review'] is None
    assert result['outcome']['final_decision'] == status
    assert result['assessment']['data']['investigation']['summary']
    assert result['executions'][0]['trajectory'][-3:] == ['investigate_claim', 'assess', 'accept_claim' if status == 'accepted' else 'reject_claim']
    events = {e['event_type'] for e in result['history']}
    assert {'ai_investigation_completed', 'autonomous_decision_recorded'} <= events


async def test_technical_failure_stays_undecided(service, settings):
    settings.decision_mode = 'autonomous'
    class Broken(MockProvider):
        async def generate(self, request):
            raise RuntimeError('Temporary provider outage')
    with pytest.raises(DomainError):
        await process_claim(service, 'CLM-001', 1, settings, provider=Broken())
    result = service.detail('CLM-001')
    assert result['status'] == 'submitted' and result['outcome'] is None
    assert result['executions'][0]['status'] == 'failed'


async def test_unknown_investigation_sources_fail_safely(service, settings):
    settings.decision_mode = 'autonomous'
    class Invented(MockProvider):
        async def generate(self, request):
            response = await super().generate(request)
            if request.context.get('task') == 'investigation':
                data = json.loads(response.content)
                data['evidence_ids'] = ['invented-receipt']
                response.content = json.dumps(data)
            return response
    with pytest.raises(DomainError):
        await process_claim(service, 'CLM-001', 1, settings, provider=Invented())
    assert service.detail('CLM-001')['outcome'] is None
