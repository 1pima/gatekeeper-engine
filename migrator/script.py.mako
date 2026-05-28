"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union
import os
import sqlalchemy as sa
from alembic import op

${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

# используем сообщение миграции как имя SQL-файла (без расширения)
SQL_FILE_PREFIX = "${message}"
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
