# Contributing

Keep learner edits inside the module's documented exercise file. Do not change deterministic rules, seed cases or real tests to make a solution pass. Keep modules independently runnable, commands centralized in root scripts, and mock as the default. Never commit `.env`, credentials, dependency directories or generated reports.

Run the module validation script after solving it. Reference backend tests are retained in `backend/tests`; after completing the TODOs run `(cd module-1/backend && uv run pytest -q)` (substitute the selected module number (1–4)). Some reference tests intentionally depend on the missing learner behavior and fail in the starter. PostgreSQL/Redis integration tests are opt-in; see their environment requirements in the actual test files. Frontend checks: `pnpm --dir module-1/frontend test`, `lint`, and `build`; substitute the module path as needed. Existing Playwright tests are retained and use isolated test storage.

Source reset is separate from application-data reset. Data reset scripts never change code. To discard code deliberately, first inspect `git diff`, copy your work somewhere safe, then explicitly restore only the chosen exercise file with Git. There is no automatic source reset.

Modules 3/4 use one learner file each: `app/exercises/execution.py` and `app/exercises/autonomy.py`. Their tests must exercise both allowed actions and blocked cases. Keep source/version guards, transaction controls, retry scheduling and metering outside learner edits. Module 4 data reset must clear its stable autonomous job results without flushing another module queue.
