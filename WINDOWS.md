# Windows setup — Ubuntu Bash on WSL2

Use Ubuntu on WSL2 for these exercises. The scripts use Linux utilities (`lsof`), Linux Python environments (`.venv/bin/python`), and Bash process management. Native PowerShell, Command Prompt and Git Bash are not the course runtime. You can use Windows Terminal with an Ubuntu tab.

## 1. Install WSL2 and Ubuntu

Open **PowerShell as Administrator** and run this one-time Windows command:

```powershell
wsl --install -d Ubuntu
```

Restart Windows if prompted. Open **Ubuntu** from the Start menu and create your Linux username/password. In PowerShell, check the installation:

```powershell
wsl --update
wsl --list --verbose
```

Ubuntu should show version `2`. If it shows `1`, run `wsl --set-version Ubuntu 2`. See [Microsoft's WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install).

## 2. Enable Docker in Ubuntu

Install and start [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/). Use Linux containers and the WSL2 engine. Under **Settings → Resources → WSL Integration**, enable your Ubuntu distribution and apply the change. See [Docker's WSL2 guide](https://docs.docker.com/desktop/features/wsl/).

Open an **Ubuntu terminal** and check:

```bash
docker --version
docker compose version
docker info
```

Keep Docker Desktop running. Use its WSL integration rather than installing a second Docker Engine inside Ubuntu.

## 3. Install course tools inside Ubuntu

Run all remaining commands in **Ubuntu Bash**, as your normal Linux user. Install tools here even if you already installed Windows versions of Python or Node.

```bash
sudo apt-get update
sudo apt-get install -y git curl ca-certificates lsof build-essential

# Install uv, then make it available in this terminal.
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv python install 3.12

# Install nvm and Node 24 inside Ubuntu.
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.7/install.sh | bash
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"
nvm install 24
nvm alias default 24
nvm use 24
npm install -g pnpm@11.19.0

# Verify the tools used by the course.
git --version
uv --version
uv python find 3.12
node --version
pnpm --version
command -v lsof
```

These commands follow the [uv installer](https://docs.astral.sh/uv/getting-started/installation/), [uv Python installation guide](https://docs.astral.sh/uv/guides/install-python/), and [nvm installation guide](https://github.com/nvm-sh/nvm/tree/v0.40.7#installing-and-updating). Node 24 satisfies the course's Node requirement.

## 4. Clone inside your Linux home directory

Keep the checkout under `~/projects` in Ubuntu. Use the same Ubuntu checkout for setup, editing and validation; do not reuse a Windows-created `.venv` or `node_modules` directory.

```bash
mkdir -p ~/projects
cd ~/projects
git -c core.autocrlf=false clone https://github.com/vishrut-pdg/incture-enterprise-ai-exercises.git
cd incture-enterprise-ai-exercises
bash scripts/doctor.sh 1 --prerequisites
```

If GitHub requests authentication, use an account with access to the exercise repository. Do not paste credentials into course files.

## 5. Set up and start Module 1

In the first Ubuntu terminal, from the repository root:

```bash
bash scripts/setup-module1.sh
bash scripts/doctor.sh 1
bash scripts/start-module1.sh
```

Open http://localhost:5173 in your Windows browser. Backend health is at http://localhost:8000/api/health. Read [Module 1's exercise](module-1/EXERCISE.md) and edit only its allowed file. Mock mode needs no cloud credentials or Ollama.

Open a **second Ubuntu terminal** to validate:

```bash
cd ~/projects/incture-enterprise-ai-exercises
bash scripts/test-module1.sh
```

Starter validation intentionally fails until you implement the learner TODOs. Success ends with `MODULE 1 EXERCISE PASSED`.

## 6. Continue to Module 2

Press **Ctrl+C in the first terminal** to stop Module 1's API, worker and frontend. From the repository root in that terminal:

```bash
bash scripts/setup-module2.sh
bash scripts/doctor.sh 2
bash scripts/start-module2.sh
```

Read [Module 2's exercise](module-2/EXERCISE.md). In the second Ubuntu terminal, after completing its TODOs:

```bash
bash scripts/test-module2.sh
```

Only one module runs on ports 5173/8000 at a time. Data and queues remain separate. Exercise PostgreSQL/Redis use ports 55432/56379.

## 7. Continue to Modules 3 and 4

Stop the previous module with Ctrl+C in its start terminal. Use the same Ubuntu checkout and installed tools. From the repository root:

```bash
bash scripts/setup-module3.sh
bash scripts/doctor.sh 3
bash scripts/start-module3.sh
# In a second Ubuntu terminal, after completing Module 3:
bash scripts/test-module3.sh
```

Stop Module 3 before starting Module 4:

```bash
bash scripts/setup-module4.sh
bash scripts/doctor.sh 4
bash scripts/start-module4.sh
# In a second Ubuntu terminal, after completing Module 4:
bash scripts/test-module4.sh
```

Module 3 uses Run for controlled execution and retains manager review for uncertainty. Module 4 starts autonomous discovery automatically; it has no Run/approval step. Its untouched TODO starter safely records failed processing until implemented.

## 8. Reset application data

Stop the running module with Ctrl+C first. Choose the module you want to reset:

```bash
bash scripts/reset-module1.sh
# Or, for Module 2:
bash scripts/reset-module2.sh
# Or, for the later modules:
bash scripts/reset-module3.sh
bash scripts/reset-module4.sh
```

These commands preserve learner source code. After reset, use that module's start command again.

## Windows troubleshooting

| Symptom | Check and fix |
| --- | --- |
| `lsof` missing or `.venv/bin/python` missing | Confirm you are in Ubuntu, not Git Bash. Install `lsof` using step 3 and run setup inside the Ubuntu checkout. |
| `uv`, `node` or `pnpm` not found | Reopen Ubuntu after installation. For the current terminal, source the uv/nvm files from step 3 and run `nvm use 24`. |
| Docker command missing or daemon unreachable | Start Docker Desktop, enable Ubuntu WSL Integration, then reopen Ubuntu and run `docker info`. |
| `/usr/bin/env: bash\r` or `$'\r': command not found` | The file has Windows CRLF line endings. Save affected `.sh` files with LF in your editor. The repository enforces LF for shell scripts through `.gitattributes`. |
| `Permission denied` when a wrapper launches another script | From the Ubuntu repository root, run `chmod +x scripts/*.sh`, then retry with `bash scripts/setup-module1.sh`. |
| Port 5173 or 8000 already occupied | Stop the other module in its start terminal. On Windows, a Windows application may also own the port; inspect `netstat -ano` in PowerShell and stop the identified application normally. |
| Browser cannot open the app | Confirm the first Ubuntu terminal is still running, check `curl http://localhost:8000/api/health` inside Ubuntu, and inspect [troubleshooting](TROUBLESHOOTING.md). |

Windows-specific commands were checked against official installation documentation. Native execution on a Windows/WSL2 machine has not been verified in this macOS workspace.
