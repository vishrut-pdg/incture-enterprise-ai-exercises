# Course guide

Do not start by reading every file. Follow one claim through the application.

Module 1 uses **CLM-003**, a $62 taxi expense. Travel is allowed and the amount is within policy, but no receipt exists. `receipt_required` is a deterministic finding. AI summarizes these facts, never invents evidence and never recommends a business action.

Module 2 uses **CLM-001** (client lunch → Accept), **CLM-002** (personal entertainment → Reject), and **CLM-003** (missing receipt → Reject in the reference behavior). Every recommendation still creates a manager review, never a final decision.

## Recommended order

Paths below are relative to `module-1/` or `module-2/`:

1. `frontend/src/features/claims/ClaimDetail.tsx` — what the learner sees.
2. `backend/app/api/routes.py` — HTTP request entry.
3. `backend/app/assessment/service.py` — source facts and business state.
4. `backend/app/domain/policy.py` — deterministic checks.
5. `backend/app/workflows/process_claim.py` — execution and safe failures.
6. `backend/app/agents/claim_agent.py` — bounded retrieval trajectory.
7. `backend/app/tools/claims.py` — agent-accessible service methods.
8. `backend/app/ai/gateway.py` — provider-neutral inference, metering and validation.
9. `backend/app/ai/providers/mock.py` — repeatable local model response.
10. `backend/app/db/repositories/claims.py` and `db/models/` — persisted records.

Learner edits are `app/exercises/summary.py` (Module 1), `app/exercises/recommendation.py` (Module 2), `app/exercises/execution.py` (Module 3) and `app/exercises/autonomy.py` (Module 4). Search `TODO(MODULE1)` or `TODO(MODULE2)` in the corresponding module. There are four and three TODOs respectively. Expect roughly 20–40 meaningful lines, rather than a plumbing project.

## Provider path

All four `.env.example` files default to `LLM_PROVIDER=mock`, `RAG_ENABLED=false` and mock embeddings. Mock needs no credentials or network inference. Optional Ollama: install it, run `ollama serve`, run `ollama pull` with the `LLM_MODEL` value from your module .env, set `LLM_PROVIDER=ollama`, and restart the app. Vertex and BTP adapters are retained reference infrastructure. Their optional dependencies and credentials are outside the exercise golden path.

Optional policy retrieval uses `docs/policies/README.md`. Set `RAG_ENABLED=true` and `EMBEDDING_PROVIDER=mock`, then rerun setup to index it. Cloud embeddings are optional. No RAG index is needed when retrieval is disabled.

## Provided infrastructure

Schemas, migrations, policy rules, seed data, repositories, provider adapters, manager role scaffolding, workers, usage metering and unrelated frontend code are provided. Inspect them if curious. Do not modify them to force an exercise test to pass.

## Common mistakes

Module 1: asking the model if a receipt exists; calculating policy inside a prompt; passing ORM objects; inventing evidence IDs; adding recommendations. Module 2: arbitrary recommendation strings; missing source validation; finalizing claims from AI advice; bypassing Pydantic; calling Ollama or Vertex directly instead of the gateway.

## Module 3 — Execute with controls

Follow CLM-001, CLM-002 and CLM-003 through `ClaimService.finish` into `app/exercises/execution.py`. Complete four `TODO(MODULE3)` markers. Confidence, policy permissions, deterministic findings and evidence coverage decide eligibility. The application executes only eligible advice; other cases still need a manager. Historical reviewed outcomes cannot override current rules.

## Module 4 — Investigate and decide autonomously

Follow the worker's `scan_claims`, `ClaimAgent` investigation stage, gateway validation and `ClaimService.autonomous_assessment` into `app/exercises/autonomy.py`. Complete four `TODO(MODULE4)` markers. Both stages must substantiate acceptance; the supplied autonomous policy rejects unmet requirements, including missing receipts. Failed inference/validation remains undecided for technical retry. Discovery, scheduling, logging and database writes are provided.

Do not copy your earlier learner files into later starters. Each module starts with the earlier capabilities completed. Only one module runs on the shared application ports at a time; every module has its own database and queue. Use the corresponding setup/start/test/reset wrapper numbered 1–4.
