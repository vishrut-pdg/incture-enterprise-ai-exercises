# Troubleshooting

**Windows:** use [Ubuntu Bash on WSL2](WINDOWS.md). That guide covers installation, Docker integration, missing commands, LF line endings and all four modules.

Run commands from the repository root. Examples use Module 1; substitute the selected module number (1–4) in paths and wrappers when needed. Begin with `./scripts/doctor.sh 1`. Stop the application with Ctrl+C before resetting or switching modules.

## Docker is not running

Symptom: setup cannot contact Docker. Check: `docker info`. Cause: Docker Desktop is stopped. Fix: start Docker Desktop, then rerun `./scripts/setup-module1.sh`.

## PostgreSQL or Redis is unavailable

Symptom: connection refused, failed assessment submission, or doctor reports unavailable storage. Check: `docker compose -p incture-exercises logs postgres redis`. Cause: exercise containers are stopped or ports are occupied. Fix: `docker compose -p incture-exercises up -d --wait postgres redis`, then rerun setup. Ports are 55432 and 56379, not the demo's 5432/6379.

## Backend does not start

Symptom: http://localhost:8000/api/health does not load. Check: `./scripts/doctor.sh 1` and the start command logs. Cause: missing dependencies, .env, migration or an occupied port. Fix: `./scripts/setup-module1.sh`, then `./scripts/start-module1.sh`.

## Frontend does not start / application does not open

Symptom: http://localhost:5173 does not load. Check: `node --version`, `pnpm --version`, and `lsof -nP -iTCP:5173 -sTCP:LISTEN`. Cause: dependencies missing, unsupported Node or frontend stopped. Fix: use Node 22.12+ / 24 LTS and rerun setup/start. A blank UI can also mean the API is stopped; inspect the start logs and health URL.

## Worker is not running / job remains pending

Symptom: processing never completes. Check the ARQ log in the start terminal. Cause: no worker, wrong queue, Redis unavailable or a stale worker with another .env. Fix: Ctrl+C to stop all managed processes, verify `ARQ_QUEUE_NAME=exercises-module1` in `module-1/.env`, run doctor, and restart. API and worker must use the same module configuration. If a previous job is stuck, stop the application and reset module data before retrying. Do not run a second unmanaged worker.

## Port already in use

Symptom: start refuses to run or Docker cannot bind. Check each required port:

```bash
lsof -nP -iTCP:5173 -sTCP:LISTEN
lsof -nP -iTCP:8000 -sTCP:LISTEN
lsof -nP -iTCP:55432 -sTCP:LISTEN
lsof -nP -iTCP:56379 -sTCP:LISTEN
```

Cause: another module, demo application or service is running. Fix: stop the owner using its own terminal or service manager. Do not blindly kill processes. Exercise data services use separate ports; application ports are shared and only one app runs at a time.

## .env missing / wrong provider configured

Symptom: doctor reports .env missing or the app requests cloud credentials. Check: compare `module-1/.env` with `.env.example` locally; do not share secrets. Cause: missing environment file or provider changed. Fix: run setup to create the missing file; set `LLM_PROVIDER=mock` and `RAG_ENABLED=false` for the golden path, then restart. Setup preserves an existing .env rather than overwriting it.

## Ollama unavailable / model missing

Symptom: provider health or inference fails after opting into Ollama. Check: `ollama list`. Cause: service stopped or configured model not pulled. Fix: `ollama serve`, then `ollama pull` with the module .env's LLM_MODEL value. Alternatively set `LLM_PROVIDER=mock` and restart; Ollama is optional.

## Database not migrated / seed data missing

Symptom: missing table errors or CLM-001 through CLM-007 are absent. Check: doctor reports whether PostgreSQL is migrated and CLM-003 exists. Cause: setup did not finish or database URL was changed. Fix: restore the database/Redis settings from that module's .env.example, then run `./scripts/setup-module1.sh`. Setup uses bootstrap, `alembic upgrade head`, and `python -m app.seed` from the reference implementation. Repeated setup preserves existing decisions. To restore fresh data, stop the app and use `./scripts/reset-module1.sh`.

## RAG index missing

Symptom: optional retrieved policy passages are absent or retrieval fails. Check: confirm RAG_ENABLED. Cause: retrieval enabled without indexing or embedding provider credentials. Fix: for a local experiment set `RAG_ENABLED=true` and `EMBEDDING_PROVIDER=mock`, then rerun setup. Manual command: `(cd module-1/backend && uv run python -m app.rag.index --if-needed)`. Data reset clears the index; reindex afterwards. No index is required when RAG_ENABLED=false.

## AI returns schema validation error / unknown finding or evidence ID

Symptom: failed processing history or a course validation failure. Check: `./scripts/test-module1.sh`; inspect the original failure in claim execution history. Cause: missing required fields, extra fields, invalid confidence/recommendation, or invented references. Fix: implement strict Pydantic parsing and compare IDs against supplied context. Module 1 forbids recommendation. Module 2 permits only lowercase accept/reject. Do not relax tests or fabricate evidence.

## Processing fails in the untouched starter

Symptom: "Assessment failed safely" when clicking Run. Check the execution history. Cause: learner boundary deliberately raises "exercise incomplete". Fix: complete the module's marked file and run validation. Browsing, chat, infrastructure and the usage dashboard are provided; successful processing is the exercise outcome.

## UI does not reflect assessment

Symptom: the queue or detail screen looks unchanged. Check the execution status and API health. Cause: worker has not finished, model validation failed, a cached query is stale, or you are looking at another module. Fix: wait for processing, refresh the claim page, inspect history, and confirm the visible module indicator. Do not directly modify database status.

## Stale process after changing configuration

Symptom: provider or queue still reflects old settings. Check which start terminal is running. Cause: settings are cached and existing processes keep their old environment. Fix: Ctrl+C, then rerun `./scripts/start-module1.sh`. It starts API, worker and frontend together.

## Three-terminal fallback

If you prefer separate logs, run setup, then these commands from the repository root in three terminals. Stop all three before changing module/configuration or resetting:

```bash
(cd module-1/backend && uv run uvicorn app.main:app --host 127.0.0.1 --port 8000)
(cd module-1/backend && uv run arq app.jobs.worker.WorkerSettings)
(cd module-1/frontend && pnpm dev --host 127.0.0.1 --port 5173 --strictPort)
```

## Reset data versus reset code

`./scripts/reset-module1.sh` resets only the selected module's application data. It refuses unexpected database/Redis settings. Stop all API/worker/frontend processes first, including any fallback terminals. It never resets learner source. Save work and explicitly restore a selected file with Git only if you intentionally want to discard code changes.

## Module 3 does not automatically execute a recommendation

Check confidence, unresolved questions, policy permissions, current check severity and cited evidence. Automatic acceptance needs all checks passing and complete evidence; rejection needs a cited deterministic rejection finding. CLM-003 goes to manager review. Run `bash scripts/test-module3.sh` and inspect `module-3/DEBUGGING.md` before changing infrastructure.

## Module 4 has no Run button / claims remain undecided

The worker discovers claims at startup and every five seconds. Check its heartbeat and execution history. An untouched starter fails at `resolve_assessment`; complete `TODO(MODULE4)` and run `bash scripts/test-module4.sh`. Technical failures stay undecided and retry after cooldown (300 seconds by default). To retry immediately with fresh seed data, stop the app, run `bash scripts/reset-module4.sh`, then restart. Reset clears only this module's stable autonomous job keys. Both stages must substantiate acceptance; missing receipt requirements follow the supplied rejection policy. Do not fabricate evidence or add a manager approval step.
