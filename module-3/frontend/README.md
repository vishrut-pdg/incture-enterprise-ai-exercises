# Provided frontend — Module 3

Start from the repository root with `bash scripts/start-module3.sh` after setup. Windows uses [Ubuntu Bash on WSL2](../../WINDOWS.md). Learners edit only the module's documented backend exercise file.

From the repository root:

```bash
pnpm --dir module-3/frontend test
pnpm --dir module-3/frontend lint
pnpm --dir module-3/frontend build
# After completing the learner TODOs, with Redis available:
pnpm --dir module-3/frontend exec playwright test
```

The browser tests use temporary storage and separate ports/queues. Use Run in Claim queue for controlled batch execution.
