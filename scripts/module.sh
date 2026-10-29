#!/usr/bin/env bash
# Canonical operations. Wrappers select a module; run from any working directory.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
module="${1:?module required}"; operation="${2:?operation required}"
[[ "$module" =~ ^[1-4]$ ]] || { echo 'Choose module 1, 2, 3 or 4'; exit 1; }
APP="$ROOT/module-$module"
compose() { docker compose -p incture-exercises -f "$ROOT/docker-compose.yaml" "$@"; }
py() { (cd "$APP/backend" && uv run "$@"); }
idle() {
 for port in 8000 5173; do
  if lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
   echo "[FAIL] Port $port is occupied. Stop the running application before $operation."
   echo "Check: lsof -nP -iTCP:$port -sTCP:LISTEN"; exit 1
  fi
 done
}
case "$operation" in
 setup)
  "$ROOT/scripts/doctor.sh" "$module" --prerequisites
  [[ -f "$APP/.env" ]] || cp "$APP/.env.example" "$APP/.env"
  compose up -d --wait postgres redis
  (cd "$APP/backend" && uv sync --frozen)
  (cd "$APP/frontend" && pnpm install --frozen-lockfile)
  py python -m app.bootstrap
  py alembic upgrade head
  py python -m app.seed
  py python -c 'from app.config import get_settings; import subprocess; s=get_settings(); subprocess.run(["python","-m","app.rag.index","--if-needed"],check=True) if s.rag_enabled else None'
  printf '\nMODULE %s SETUP COMPLETE\nNext: ./scripts/start-module%s.sh\n' "$module" "$module"
 ;;
 start)
  idle
  [[ -x "$APP/backend/.venv/bin/python" && -d "$APP/frontend/node_modules" && -f "$APP/.env" ]] || { echo "Run ./scripts/setup-module$module.sh first."; exit 1; }
  "$ROOT/scripts/doctor.sh" "$module" --runtime
  children=()
  cleanup() {
   trap - EXIT INT TERM
   for pid in "${children[@]}"; do kill -TERM "$pid" 2>/dev/null || true; done
   for pid in "${children[@]}"; do wait "$pid" 2>/dev/null || true; done
   echo 'API, worker and frontend stopped.'
  }
  trap cleanup EXIT; trap 'exit 130' INT; trap 'exit 143' TERM
  (cd "$APP/backend" && exec .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000) & children+=("$!")
  (cd "$APP/backend" && exec .venv/bin/python -m arq app.jobs.worker.WorkerSettings) & children+=("$!")
  (cd "$APP/frontend" && exec node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173 --strictPort) & children+=("$!")
  printf '\nFrontend: http://localhost:5173\nBackend: http://localhost:8000\nHealth: http://localhost:8000/api/health\nModule: %s\nProvider: ' "$module"
  py python -c 'from app.config import get_settings; print(get_settings().llm_provider)'
  echo 'Ctrl+C stops all three processes.'
  while true; do
   for pid in "${children[@]}"; do kill -0 "$pid" 2>/dev/null || { echo 'A component stopped; check its log above.'; exit 1; }; done
   sleep 1
  done
 ;;
 test)
  [[ -x "$APP/backend/.venv/bin/python" ]] || { echo "Run ./scripts/setup-module$module.sh first."; exit 1; }
  py python "$ROOT/scripts/validate.py" "$module"
 ;;
 reset)
  idle
  echo "Resetting Module $module application data. Source code is preserved."
  py python -m app.course_reset
  printf 'MODULE %s DATA RESET\nNext: ./scripts/start-module%s.sh\n' "$module" "$module"
 ;;
 *) echo 'Unknown operation'; exit 1 ;;
esac
