"""Create only this exercise module's database; called by setup, never by agents."""
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.config import get_settings


def main():
    url = make_url(get_settings().database_url)
    if url.database != "exercises_module4" or url.port != 55432 or url.host not in {"localhost", "127.0.0.1"}:
        raise ValueError("Use the module .env.example database on local exercise port 55432")
    admin = create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    try:
        with admin.connect() as connection:
            if not connection.scalar(text("SELECT 1 FROM pg_database WHERE datname=:name"), {"name": url.database}):
                name = connection.dialect.identifier_preparer.quote_identifier(url.database)
                connection.execute(text("CREATE DATABASE " + name))
        print("Module database ready")
    finally:
        admin.dispose()


if __name__ == "__main__":
    main()
