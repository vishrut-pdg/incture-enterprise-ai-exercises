# AI usage and performance — Module 4

Open **AI usage & performance** in the sidebar or visit `#/analytics`. It shows claim runs, model requests, provider/model groups, latency, errors and available token/cost metadata. It never starts claim processing. Setup automatically applies its migration to this module database, `exercises_module4`.

Usage telemetry shows how the AI runtime is operating. It does not tell us by itself whether the AI response is correct.

## Reading the dashboard

A claim run is the complete workflow recorded in `ai_executions`, including retries and failures. Manager decisions do not count as model requests. A model request is an investigation, assessment, chatbot call or optional document/query embedding. Autonomous processing normally makes separate investigation and assessment requests. Missing usage metadata is shown as unavailable. Costs are estimates using configured rates, not a cloud billing report. Mock and Ollama have no provider API charge; machine and hosting costs are excluded.

Validation failures can still incur provider usage. Transport failures without usage metadata remain unpriced. Logs retain failure information without storing credentials. The course deliberately leaves metering outside learner edits.

## Code walkthrough

- `backend/app/analytics/metering.py`: normalizes usage and records latency/outcome.
- `backend/app/ai/gateway.py`: meters provider execution and validation.
- `backend/app/assistant/service.py` and `backend/app/rag/embeddings.py`: chat/embedding measurements.
- `backend/app/analytics/service.py`: read-only totals, provider groups and request history.
- `backend/app/db/models/__init__.py` and `backend/migrations/versions/20261009_ai_usage.py`: storage.
- `frontend/src/features/analytics/AIUsage.tsx`: dashboard UI.

For another model or contracted rate, set `AI_COST_RATES` to provider/model rates in the module .env, then restart. Preserve the existing configuration validation. No telemetry implementation is required for the exercise.
