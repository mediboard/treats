"""increase character length

Revision ID: da8645cc476f
Revises: 19889d69f95d
Create Date: 2023-02-12 09:57:11.738663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da8645cc476f'
down_revision = '19889d69f95d'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('conditions', 'name', type_=sa.String(length=200))


def downgrade():
    op.alter_column('conditions', 'name', type_=sa.String(length=150))
