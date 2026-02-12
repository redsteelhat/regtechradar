"""Alembic environment — DATABASE_URL from env or .env."""
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# DATABASE_URL kullan (sync URL; Alembic sync çalışır)
import os

try:
    from src.config import settings
    database_url = settings.database_url
except Exception:
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://regtech:regtech@localhost:5432/regtechradar",
    )

config.set_main_option("sqlalchemy.url", database_url)

target_metadata = None  # Autogenerate için model'leri import edip buraya bağlayabiliriz


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
