"""add cluster name into effects

Revision ID: cb78ee4465c7
Revises: a0b22bba7ecd
Create Date: 2022-09-06 11:53:58.955774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb78ee4465c7'
down_revision = 'a0b22bba7ecd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('effects', sa.Column('cluster_name', sa.String(length=100), nullable=True))


def downgrade():
    op.drop_column('effects', 'cluster_name')
