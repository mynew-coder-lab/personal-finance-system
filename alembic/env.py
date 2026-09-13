"""
Alembic migration environment.

Configured to:
- Read DATABASE_URL from app settings (not alembic.ini)
- Auto-discover all models via Base.metadata
- Support both offline and online migration modes
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

from app.backend.config import settings
from app.backend.database.database import Base

# Import all models here so Alembic can detect them for autogenerate.
# As new models are added, import them below:
from app.backend.models import *  # noqa: F401, F403

# Alembic Config object
config = context.config

# Override sqlalchemy.url from our application settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Python logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no live DB connection)."""
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
    """Run migrations in 'online' mode (live DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
