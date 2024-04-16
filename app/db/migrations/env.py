import asyncio
import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import get_settings  # isort:skip
from app.db.base import Base

SETTINGS = get_settings()
DATABASE_URL = SETTINGS.DB_URL

config = context.config

fileConfig(config.config_file_name)  # type: ignore

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", str(DATABASE_URL))


def process_revision_directives(ctx, revision, directives) -> None:
    if ctx.config.cmd_opts.autogenerate:
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        ),
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


asyncio.run(run_migrations_online())
