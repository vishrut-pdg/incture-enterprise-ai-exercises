# Instructor / solution reference — Module 3

Outside the normal learner flow. Intended changes: implement the four TODOs in `backend/app/exercises/execution.py`. The task isolates the decision boundary from provided transaction, inference and worker infrastructure.

Checkpoints: CLM-001 is accepted, CLM-002 rejected, and CLM-003 sent to manager review. Common mistakes include trusting model confidence without evidence, ignoring policy flags, mutating source context and writing database state from the learner function. Automatic rejection requires a cited deterministic rejection finding; otherwise escalate.

Tests cover positive and negative decisions, confidence boundaries, evidence coverage, source immutability, end-to-end outcomes and audit. Retained reference tests cover concurrency, invalid model output, worker behavior and source changes. No runnable solution is included in the starter.
