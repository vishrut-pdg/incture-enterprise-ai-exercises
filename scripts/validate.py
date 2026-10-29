"""Friendly requirement-level wrapper around real pytest assertions, no solution code."""
import subprocess
import sys

module = sys.argv[1]
checks = {
 '1': [
  ('Claim facts and policy context included without source mutation', 'test_claim_and_policy', 'Copy source facts, not ORM objects. Keep source dictionaries independent.'),
  ('Missing receipt finding and evidence included', 'test_missing_receipt_and_evidence', 'Use supplied checks unchanged. Do not recalculate policy or invent a receipt.'),
  ('Optional passages and prior context preserved', 'test_optional_passages', 'Preserve optional grounded passages when supplied.'),
  ('Factual output and evidence references validated', 'test_valid_factual_output', 'Parse the Assessment schema and validate known source references.'),
  ('Unknown evidence and finding IDs rejected', 'test_unknown_references', 'Compare output IDs against context evidence and checks.'),
  ('AI output contains no decision recommendation', 'test_no_recommendation', 'Use the strict facts-only schema, including extra-field rejection.'),
  ('CLM-003 remains a human decision', 'test_human_owns_claim', 'Complete both learner functions; do not modify manager workflow.'),
 ],
 '2': [
  ('Structured recommendation generated', 'test_structured_advice', 'Parse the strict Assessment schema and return validated advice.'),
  ('CLM-001 Accept; CLM-002 and CLM-003 Reject; manager review remains required', 'test_hero_cases', 'Preserve the reference recommendation and manager workflow.'),
  ('Recommendation references known findings', 'test_unknown_findings', 'Reject codes absent from context checks.'),
  ('Evidence references valid, including missing receipt case', 'test_unknown_evidence', 'Reject IDs absent from context evidence, including when it is empty.'),
  ('Invalid recommendation values and contracts rejected', 'test_invalid_contract', 'Use strict Pydantic validation, not a permissive dictionary.'),
 ],
}
checks['3'] = [
 ('Eligible advice selects the correct action without writes', 'test_action_selection', 'Return accept/reject/review; keep source inputs unchanged.'),
 ('Confidence threshold and unresolved questions respected', 'test_confidence_and_questions', 'Automation needs confidence >= 0.90 and no unresolved questions.'),
 ('Policy permissions enforced', 'test_policy_permissions', 'Read the current policy auto_accept and auto_reject flags.'),
 ('Acceptance requires complete evidence and passing checks', 'test_evidence_coverage', 'Compare all cited evidence IDs and all current checks.'),
 ('Rejection requires a cited deterministic rejection finding', 'test_rejection_requires_cited_failure', 'A model rejection alone is insufficient for automatic rejection.'),
 ('CLM-001 accepted, CLM-002 rejected, CLM-003 sent to review', 'test_workflow_outcomes', 'Select actions only; ClaimService owns state changes and audit.'),
]
checks['4'] = [
 ('Both grounded model stages support acceptance', 'test_supported_acceptance', 'Return a new assessment rather than mutating source data.'),
 ('Missing receipt cannot be overridden by model text', 'test_missing_receipt_cannot_be_invented', 'Non-pass deterministic checks must block acceptance and explain why.'),
 ('Uncertainty and stage disagreement prevent acceptance', 'test_uncertainty_and_disagreement', 'Inspect confidence, limitations and unresolved questions from both stages.'),
 ('Complete evidence and policy permissions required', 'test_evidence_coverage_and_policy', 'Both stages must cite all evidence; blocked rejection raises ValueError.'),
 ('Autonomous outcomes retain investigation and audit without review', 'test_autonomous_outcomes_and_audit', 'Return a binary result under the course policy; persistence stays in ClaimService.'),
 ('Technical failure leaves the claim undecided', 'test_technical_failure_stays_undecided', 'Provider failures are handled by the existing workflow, never converted into rejection.'),
 ('Invented investigation sources rejected', 'test_unknown_investigation_sources_fail_safely', 'Gateway and service source validation are provided infrastructure.'),
]
learner_files = {'1': 'summary', '2': 'recommendation', '3': 'execution', '4': 'autonomy'}
print(f'MODULE {module} VALIDATION\n', flush=True)
failed = []
for label, test, hint in checks[module]:
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', f'tests/test_course.py::{test}', '--tb=short'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f'[PASS] {label}', flush=True)
    else:
        print(f'[FAIL] {label}\n\nCheck: backend/app/exercises/{learner_files[module]}.py\nHint: {hint}\n', flush=True)
        failed.append(test)
if failed:
    print('For detailed assertions: uv run pytest tests/test_course.py --tb=short')
    sys.exit(1)
print(f'\n================================\nMODULE {module} EXERCISE PASSED\n================================')
