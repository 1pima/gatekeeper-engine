from logging.config import fileConfig

from sqlalchemy import create_engine
from flask import current_app
from alembic import context

from internal.factory import new_app

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None

app = new_app()


def get_migration_db_url():
    """Получаем специальный URI для миграций из конфига Flask."""
    # Ищем URI пользователя с правами на миграции. Если его нет — фоллбэк на основной.
    migration_uri = current_app.config.get('SQLALCHEMY_MIGRATION_URI')
    if not migration_uri:
        migration_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI')

    if not migration_uri:
        raise ValueError("Database URI not found in Flask application config.")

    return migration_uri


def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме."""
    with app.app_context():
        url = get_migration_db_url()
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в online-режиме с использованием контекста Flask."""
    with app.app_context():
        url = get_migration_db_url()

        # Создаем engine напрямую из полученного URL
        connectable = create_engine(url)

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()