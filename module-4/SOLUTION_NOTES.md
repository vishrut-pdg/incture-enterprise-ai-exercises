# Instructor / solution reference — Module 4

Outside the normal learner flow. Intended changes: implement the four TODOs in `backend/app/exercises/autonomy.py`. The task isolates the decision boundary from provided transaction, inference and worker infrastructure.

Checkpoints: The worker discovers claims automatically. CLM-001 is accepted; CLM-002 and CLM-003 are rejected after investigation. No manager review is created. Common mistakes include trusting model confidence without evidence, ignoring policy flags, mutating source context and writing database state from the learner function. Both stages must support acceptance. Unmet requirements follow the supplied autonomous rejection policy; technical failures remain undecided. Never invent evidence or erase the stored investigation limitations.

Tests cover positive and negative decisions, confidence boundaries, evidence coverage, source immutability, end-to-end outcomes and audit. Retained reference tests cover concurrency, invalid model output, worker behavior and source changes. No runnable solution is included in the starter.
