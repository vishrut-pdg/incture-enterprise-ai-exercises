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
print(f'MODULE {module} VALIDATION\n', flush=True)
failed = []
for label, test, hint in checks[module]:
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', f'tests/test_course.py::{test}', '--tb=short'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f'[PASS] {label}', flush=True)
    else:
        print(f'[FAIL] {label}\n\nCheck: backend/app/exercises/{"summary" if module=="1" else "recommendation"}.py\nHint: {hint}\n', flush=True)
        failed.append(test)
if failed:
    print('For detailed assertions: uv run pytest tests/test_course.py --tb=short')
    sys.exit(1)
print(f'\n================================\nMODULE {module} EXERCISE PASSED\n================================')
