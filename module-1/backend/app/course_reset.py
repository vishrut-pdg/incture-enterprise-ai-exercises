"""Reset this dedicated module's application data; never restore learner source."""
from sqlalchemy import delete
from sqlalchemy.engine import make_url
from redis import Redis
from app.config import get_settings
from app.db.models import Base
from app.db.session import SessionLocal
from app.seed import seed


def main():
    s = get_settings()
    db, redis = make_url(s.database_url), make_url(s.redis_url)
    if db.database != "exercises_module1" or db.port != 55432 or db.host not in {"localhost", "127.0.0.1"}:
        raise ValueError("Reset refused: restore this module's .env.example database URL")
    if redis.port != 56379 or redis.host not in {"localhost", "127.0.0.1"} or s.arq_queue_name != "exercises-module1":
        raise ValueError("Reset refused: restore this module's .env.example Redis URL and queue")
    queue = Redis.from_url(s.redis_url, socket_connect_timeout=3)
    # Application processes must be stopped first. Only remove this module's queued jobs.
    if queue.exists(s.arq_queue_name + ":health-check"):
        raise ValueError("Reset refused: stop this module's worker, wait for heartbeat expiry, then retry")
    jobs = queue.zrange(s.arq_queue_name, 0, -1)
    if jobs:
        queue.delete(*["arq:job:" + j.decode() for j in jobs])
    queue.delete(s.arq_queue_name)
    with SessionLocal() as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(delete(table))
        session.commit()
        seed(session)
    print("Seeded claims restored; learner source preserved. Reindex if RAG is enabled.")


if __name__ == "__main__":
    main()
