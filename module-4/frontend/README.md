# Provided frontend — Module 4

Start from the repository root with `bash scripts/start-module4.sh` after setup. Windows uses [Ubuntu Bash on WSL2](../../WINDOWS.md). Learners edit only the module's documented backend exercise file.

From the repository root:

```bash
pnpm --dir module-4/frontend test
pnpm --dir module-4/frontend lint
pnpm --dir module-4/frontend build
# After completing the learner TODOs, with Redis available:
pnpm --dir module-4/frontend exec playwright test
```

The browser tests use temporary storage and separate ports/queues. Autonomous processing begins without Run or manager approval controls.
