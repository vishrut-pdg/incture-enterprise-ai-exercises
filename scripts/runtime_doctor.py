"""Report non-secret runtime checks; hide normal dependency exception traces."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / f"module-{sys.argv[1]}" / "backend"))
from urllib.request import urlopen
import json

failures = 0

def check(label, call, fix):
    global failures
    try:
        call()
        print(f'[PASS] {label}')
    except Exception:
        print(f'[FAIL] {label}\n       Why: required runtime dependency is unavailable.\n       Fix: {fix}')
        failures += 1

try:
    from app.config import get_settings
    from sqlalchemy import create_engine, text
    from redis import Redis
    s = get_settings()
except Exception:
    print('[FAIL] Backend dependencies/configuration invalid. Fix: rerun setup; compare .env with .env.example')
    sys.exit(1)
module = sys.argv[1]
from sqlalchemy.engine import make_url
url, redis_url = make_url(s.database_url), make_url(s.redis_url)
if (url.database != f'exercises_module{module}' or url.host not in {'localhost', '127.0.0.1'} or url.port != 55432 or redis_url.host not in {'localhost', '127.0.0.1'} or redis_url.port != 56379 or s.arq_queue_name != f'exercises-module{module}'):
    print('[FAIL] Unexpected module data configuration. Fix: restore database/Redis/queue values from this module .env.example')
    sys.exit(1)
print(f'[PASS] Selected provider: {s.llm_provider}')
check('Backend imports', lambda: __import__('app.main'), f'./scripts/setup-module{module}.sh')
def db():
    engine = create_engine(s.database_url, connect_args={'connect_timeout': 3})
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
            assert conn.scalar(text("SELECT count(*) FROM claims WHERE id='CLM-003'")) == 1
    finally:
        engine.dispose()
check('PostgreSQL reachable, migrated and seeded', db, f'./scripts/setup-module{module}.sh')
check('Redis reachable', lambda: Redis.from_url(s.redis_url, socket_connect_timeout=3, socket_timeout=3).ping(), f'./scripts/setup-module{module}.sh')
queue = Redis.from_url(s.redis_url, socket_connect_timeout=3, socket_timeout=3)
try:
    if queue.exists(s.arq_queue_name + ':health-check'):
        print('[PASS] Module worker heartbeat available')
    else:
        print(f'[WARN] Worker not running yet. Start with ./scripts/start-module{module}.sh')
except Exception:
    pass  # Redis failure is already reported above with its fix.
if s.llm_provider == 'ollama':
    def model():
        with urlopen(s.ollama_base_url + '/api/tags', timeout=3) as r:
            assert s.llm_model in [m['name'] for m in json.load(r)['models']]
    check('Configured Ollama model available', model, f'ollama serve; ollama pull {s.llm_model}')
elif s.llm_provider == 'mock':
    print('[PASS] Mock needs no cloud account or Ollama')
else:
    print('[WARN] Cloud provider selected. Golden path: set LLM_PROVIDER=mock in the module .env and restart.')
sys.exit(bool(failures))
