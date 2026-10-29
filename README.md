# Enterprise AI Building Blocks
## Hands-on Exercises

### What this repository is

The instructor shows the complete demo application. This repository is where learners code inside the same architecture. It provides **Modules 1–4** as independent learner exercises, derived from the instructor references.

### Course progression

| Module | Goal | Boundary you implement |
| --- | --- | --- |
| 1 — Understand and Retrieve | What is true about this claim? | Facts + policy + evidence → grounded factual summary |
| 2 — Assess and Explain | What should we do? | Grounded context → validated Accept/Reject recommendation |
| 3 — Execute | When may the application act? | Validated advice → eligible execution or manager review |
| 4 — Autonomous | How can the workflow resolve claims itself? | Grounded investigation + assessment → bounded automatic decision |

### Fastest path

**Windows users:** complete the [Windows Bash setup](WINDOWS.md) first. Run the course commands in **Ubuntu on WSL2**. Git Bash alone does not provide the Linux tools and Python environment paths used by these scripts.

Install Git, Python 3.12, uv, Node 22.12+ (24 LTS recommended), pnpm 11.19.0 and Docker with Compose. Start Docker. No cloud account is needed.

```bash
git clone https://github.com/vishrut-pdg/incture-enterprise-ai-exercises.git
cd incture-enterprise-ai-exercises
./scripts/doctor.sh 1 --prerequisites
./scripts/setup-module1.sh
./scripts/doctor.sh
./scripts/start-module1.sh
```

Open http://localhost:5173. Read [Module 1 exercise](module-1/EXERCISE.md). Only edit its marked learner file. The UI, claim browsing, chat and dashboard run before you solve the task; processing intentionally fails safely until the TODOs are complete.

In another terminal:

```bash
./scripts/test-module1.sh
```

Get `MODULE 1 EXERCISE PASSED`. Stop the app with Ctrl+C, then continue:

```bash
./scripts/setup-module2.sh
./scripts/start-module2.sh
# In another terminal, after completing the Module 2 TODOs:
./scripts/test-module2.sh
```

Module 2 includes completed grounded retrieval. You never need to copy Module 1 code or change branches. Only one module uses application ports 5173/8000 at a time. Separate databases and queue names preserve each module's progress. Exercise PostgreSQL/Redis use **55432/56379** and Compose project `incture-exercises`.

### Continue to Modules 3 and 4

Stop the previous module with Ctrl+C before starting another. Each starter includes the earlier completed capabilities; no learner code copying or branch switching is needed.

```bash
bash scripts/setup-module3.sh
bash scripts/start-module3.sh
# In another terminal after completing module-3/EXERCISE.md:
bash scripts/test-module3.sh
```

Module 3 accepts eligible claims, rejects supported violations, and sends missing evidence or uncertainty to manager review. Stop Module 3, then continue:

```bash
bash scripts/setup-module4.sh
bash scripts/start-module4.sh
# In another terminal after completing module-4/EXERCISE.md:
bash scripts/test-module4.sh
```

Module 4's worker discovers claims automatically. Both grounded model stages must support acceptance; unmet requirements follow the supplied autonomous rejection policy. Technical failures remain undecided and retry. The untouched starter records safe failures until its TODOs are complete.

### Windows Bash commands

After the one-time [WSL2, Docker and dependency setup](WINDOWS.md), run these in an **Ubuntu** terminal, from the repository root:

```bash
bash scripts/doctor.sh 1 --prerequisites
bash scripts/setup-module1.sh
bash scripts/doctor.sh 1
bash scripts/start-module1.sh
```

In a second Ubuntu terminal, open the same repository and validate after completing the TODOs:

```bash
cd ~/projects/incture-enterprise-ai-exercises
bash scripts/test-module1.sh
```

Stop Module 1 with Ctrl+C in its start terminal before starting Module 2:

```bash
bash scripts/setup-module2.sh
bash scripts/start-module2.sh
# In the second Ubuntu terminal after completing Module 2:
bash scripts/test-module2.sh
```

To reset application data, stop the module first, then run `bash scripts/reset-module1.sh` or `bash scripts/reset-module2.sh`. Learner code is preserved. Open the app in your Windows browser at http://localhost:5173.

### Reset application data

Stop the app first. `bash scripts/reset-moduleN.sh` (replace `N` with 1, 2, 3 or 4) restores seeded claims, clears that module's queue (including stable autonomous job results for Module 4), and preserves learner source. Setup is safe to rerun and preserves existing decisions. Reset is the explicit way to start with fresh data.

### Where to go next

- [Course guide](COURSE_GUIDE.md) — follow one claim through the code.
- [Architecture](ARCHITECTURE.md) — ownership boundaries and actual paths.
- [Troubleshooting](TROUBLESHOOTING.md) — symptom, check, cause and fix.
- [Module 1](module-1/README.md) / [Module 2](module-2/README.md) / [Module 3](module-3/README.md) / [Module 4](module-4/README.md) — allowed edits and success criteria.
- [Contributing](CONTRIBUTING.md) — keep exercises small and tests meaningful.

The AI Usage & Performance dashboard is provided infrastructure. Usage telemetry shows how the AI runtime is operating. It does not tell us by itself whether the AI response is correct.
