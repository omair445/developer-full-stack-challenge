"""
Alembic migration script.
"""

import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Load environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Alembic Config object, providing access to the values within the .ini file in use
config = context.config

# Set main option for sqlalchemy URL from environment variable
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])

# Setup loggers
fileConfig(config.config_file_name)

# Add your model's MetaData object for 'autogenerate' support
from app import models

target_metadata = models.Base.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    In this scenario, an Engine must be created and a connection associated with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Main logic for running migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
