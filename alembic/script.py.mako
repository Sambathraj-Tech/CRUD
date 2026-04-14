# ============================================================
# alembic/script.py.mako
# ============================================================
# This is a Mako template file used by Alembic.
# You NEVER edit this manually.
# Alembic reads this template every time you run:
#   alembic revision --autogenerate -m "your message"
# ...and generates a new migration file in alembic/versions/
# ============================================================

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    # --- Alembic fills this in automatically ---
    # Example of what gets generated:
    #   op.create_table('users',
    #       sa.Column('id', sa.Integer(), nullable=False),
    #       sa.Column('username', sa.String(50), nullable=False),
    #       sa.PrimaryKeyConstraint('id')
    #   )
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    # --- Alembic fills this in automatically ---
    # Example of what gets generated:
    #   op.drop_table('users')
    ${downgrades if downgrades else "pass"}


# ============================================================
# HOW TO USE ALEMBIC (step by step):
#
# 1. Make sure your .env DATABASE_URL points to your DB
#
# 2. Generate your first migration after setting up models:
#    alembic revision --autogenerate -m "initial tables"
#    → Creates: alembic/versions/abc123_initial_tables.py
#
# 3. Apply the migration to the database:
#    alembic upgrade head
#
# 4. Later, if you add a new column to a model:
#    alembic revision --autogenerate -m "add phone to users"
#    alembic upgrade head
#
# 5. To roll back the last migration:
#    alembic downgrade -1
#
# 6. To see migration history:
#    alembic history
# ============================================================