"""V001_base_init

Revision ID: c1e8a861c8f0
Revises: 
Create Date: 2026-05-12 16:28:22.728844

"""
from typing import Sequence, Union
import os
import sqlalchemy as sa
from alembic import op



# revision identifiers, used by Alembic.
revision: str = 'c1e8a861c8f0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# используем сообщение миграции как имя SQL-файла (без расширения)
SQL_FILE_PREFIX = "V001_base_init"
PROJECT_ROOT = os.getcwd()
MIGRATIONS_DIR = os.path.join(PROJECT_ROOT, 'db', 'base', 'migrations')
ANTIMIGRATIONS_DIR = os.path.join(PROJECT_ROOT, 'db', 'base', 'antimigrations')

def upgrade() -> None:
    sql_path = os.path.join(MIGRATIONS_DIR, f"{SQL_FILE_PREFIX}.sql")
    if os.path.exists(sql_path):
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read().strip()
            if sql_commands:
                op.execute(sa.text(sql_commands))
    else:
        print(f"upgrade SQL file not found at {sql_path}!")


def downgrade() -> None:
    sql_path = os.path.join(ANTIMIGRATIONS_DIR, f"{SQL_FILE_PREFIX}.sql")
    if os.path.exists(sql_path):
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read().strip()
            if sql_commands:
                op.execute(sa.text(sql_commands))
    else:
        print(f"downgrade SQL file not found at {sql_path}!")
