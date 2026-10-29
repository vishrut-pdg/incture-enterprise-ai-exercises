#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
module="${1:-1}"; mode="${2:-all}"
[[ "$module" =~ ^[1-4]$ ]] || { echo 'Choose module 1, 2, 3 or 4'; exit 1; }
APP="$ROOT/module-$module"; failures=0
pass() { echo "[PASS] $*"; }
warn() { echo "[WARN] $*"; }
fail() { echo "[FAIL] $1"; echo "       Why: $2"; echo "       Fix: $3"; failures=$((failures+1)); }
need() { command -v "$1" >/dev/null 2>&1 && pass "$1 installed" || fail "$1 missing" "$2" "$3"; }
echo "Enterprise AI Course Doctor — Module $module"
need git 'Required to clone and track learner changes.' 'Install Git: https://git-scm.com/downloads'
need uv 'Runs Python and installs backend dependencies.' 'Install uv: https://docs.astral.sh/uv/getting-started/installation/'
if command -v uv >/dev/null 2>&1; then
 uv python find 3.12 >/dev/null 2>&1 && pass 'Python 3.12 available' || fail 'Python 3.12 missing' 'Backend targets Python 3.12.' 'uv python install 3.12'
fi
need node 'Runs the frontend; use Node 22.12+ or 24 LTS.' 'Install Node: https://nodejs.org/'
if command -v node >/dev/null 2>&1; then
 node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>22 || a===22&&b>=12 ? 0:1)' >/dev/null 2>&1 || fail 'Node version too old' 'Vite requires a supported Node runtime.' 'Install Node 24 LTS'
fi
need pnpm 'Installs locked frontend dependencies.' 'npm install -g pnpm@11.19.0'
need docker 'Runs PostgreSQL and Redis.' 'Install Docker Desktop: https://www.docker.com/products/docker-desktop/'
need lsof 'Checks occupied application ports.' 'Install lsof with your OS package manager'
if command -v docker >/dev/null 2>&1; then
 docker compose version >/dev/null 2>&1 && pass 'Docker Compose available' || fail 'Compose unavailable' 'Starts exercise infrastructure.' 'Install Docker Desktop with Compose'
 docker info >/dev/null 2>&1 && pass 'Docker daemon running' || fail 'Docker daemon unavailable' 'Database and queue require Docker.' 'Start Docker Desktop'
fi
for port in 8000 5173; do
 if lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then warn "Port $port occupied. Stop the server before switching modules. Check: lsof -nP -iTCP:$port -sTCP:LISTEN"; else pass "Port $port free"; fi
done
for port in 55432 56379; do
 lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1 && pass "Infrastructure port $port listening" || warn "Port $port not listening yet. Run ./scripts/setup-module$module.sh"
done
command -v ollama >/dev/null 2>&1 && pass 'Ollama installed (optional)' || warn 'Ollama missing; Mock mode works without it. Optional install: https://ollama.com/'
if [[ "$mode" != --prerequisites ]]; then
 [[ -f "$APP/.env" ]] && pass '.env exists' || fail '.env missing' 'Selects module database, queue and provider.' "./scripts/setup-module$module.sh"
 [[ -d "$APP/frontend/node_modules" ]] && pass 'Frontend dependencies installed' || fail 'Frontend dependencies missing' 'Frontend cannot start.' "./scripts/setup-module$module.sh"
 if [[ -x "$APP/backend/.venv/bin/python" ]]; then
  (cd "$APP/backend" && .venv/bin/python "$ROOT/scripts/runtime_doctor.py" "$module") || failures=$((failures+1))
 else fail 'Backend dependencies missing' 'API and worker cannot start.' "./scripts/setup-module$module.sh"; fi
fi
if [[ "$failures" -eq 0 ]]; then
 [[ "$mode" == --prerequisites ]] && echo 'PREREQUISITES READY' || echo "READY FOR MODULE $module"
else echo "$failures check(s) failed; follow the fixes above."; exit 1; fi
