# Validation record

Validated on 14 October 2026 using Python 3.12.13, the reference lockfiles, mock inference and dedicated local exercise infrastructure.

| Check | Module 1 | Module 2 |
| --- | --- | --- |
| Locked setup, database bootstrap, migrations and seed | Passed | Passed |
| Untouched learner starter | Intentional failures at its TODO boundaries | Intentional failures at its TODO boundary |
| Course-oriented validator with a completed implementation | Passed | Passed |
| Full backend suite with completed implementation | 76 passed, 4 integration checks initially skipped | 74 passed, 4 integration checks initially skipped |
| Explicit PostgreSQL concurrency and Redis/ARQ integration run | All 4 passed | All 4 passed |
| Frontend unit tests | 14 passed | 14 passed |
| Frontend lint / production build | Passed | Passed |
| Retained Playwright browser flows with completed implementation | 2 passed | 2 passed |
| Live API health, seven persisted claims and worker heartbeat | Passed | Passed |
| Application data reset and post-reset diagnostics | Passed | Passed |
| Provided infrastructure checks used by GitHub CI in untouched starter | 16 passed | 16 passed |

Completed implementations were used temporarily for verification and restored to the TODO starters before commit. No runnable learner solution is shipped. Reference tests are retained unchanged apart from course naming and isolated port references. CI runs provided infrastructure checks, collects course tests, and runs frontend checks; learner-dependent flow assertions run after completing the exercise.

The existing demo occupied ports 8000/5173. The canonical start command correctly refused to take those ports. Live exercise API/worker smoke checks used unused port 18000 and stopped their processes afterwards. Browser tests used their existing isolated ports 8001/5174 and temporary storage. Data reset was verified through its protected backend operation with exercise processes stopped; the wrapper's occupied-port guard remained enforced. No demo process was stopped and no demo file was modified.

Mock requires no cloud credentials. Live Ollama, Vertex and BTP inference were not exercised. Existing dependency deprecation notices were non-blocking. Documentation links and shell syntax checks passed.

## Modules 3 and 4 — 29 October 2026

Derived from the reference commits in SOURCE_REFERENCES.md and verified with locked Python 3.12 dependencies, mock inference and the dedicated exercise infrastructure.

| Check | Module 3 | Module 4 |
| --- | --- | --- |
| Locked setup, bootstrap, migration and seed | Passed | Passed |
| Untouched starter | 11 expected learner-boundary failures | 7 expected learner-boundary failures; 2 provided safety checks pass |
| Full backend suite with temporary completed learner code | 70 passed, 4 integration checks initially skipped | 87 passed, 5 integration checks initially skipped |
| Explicit PostgreSQL / Redis integration run | All 4 passed | All 5 passed, including autonomous concurrency |
| Course command with completed learner code | MODULE 3 EXERCISE PASSED | MODULE 4 EXERCISE PASSED |
| Frontend unit / lint / build | 14 unit tests passed; lint/build passed | 14 unit tests passed; lint/build passed |
| Retained Playwright browser journeys | 2 passed | 2 passed, including all seven claims with no human actions |
| Live starter API, seeded claims and worker heartbeat | Passed | Passed |
| Live data reset, unchanged learner source and post-reset diagnostics | Passed | Passed |
| Provided infrastructure checks in untouched starter | 16 passed | 16 passed |
| Additional autonomous reset tests | Not applicable | 5 passed: rerun safety, source preservation, worker/config guards and neighbouring job namespaces |

The temporary completed implementations were restored to the TODO starters after verification and are not committed. Additional reset tests run in GitHub CI. Live Redis checks confirmed that resetting Module 4 removes its stable autonomous job results while preserving Module 3's neighbouring namespace. Module 4 uses its supplied course policy for unmet requirements; technical/model failures stay undecided.

Existing processes occupied ports 8000/5173 during setup. Live smoke checks used port 18000 and stopped their own API/worker processes afterwards; browser tests used isolated ports 8001/5174 and temporary storage. No demo source, branch, process or data was changed. Windows documentation covers the new module commands; native WSL2 execution and live cloud/Ollama providers remain unverified here.
