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
