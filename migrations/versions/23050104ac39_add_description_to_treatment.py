"""add description to treatment

Revision ID: 23050104ac39
Revises: cb78ee4465c7
Create Date: 2022-09-06 16:25:54.615842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23050104ac39'
down_revision = 'cb78ee4465c7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('treatments', sa.Column('description', sa.String(length=5000), nullable=True))


def downgrade():
    op.drop_column('treatments', 'description')
