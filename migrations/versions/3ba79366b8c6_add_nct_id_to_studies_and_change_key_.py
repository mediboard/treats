"""add nct id to studies and change key requirements

Revision ID: 3ba79366b8c6
Revises: 3055b7729b26
Create Date: 2023-01-18 13:11:20.375715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ba79366b8c6'
down_revision = '3055b7729b26'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('studies', sa.Column('nct_id', sa.String(length=11), nullable=True))


def downgrade():
    op.drop_column('studies', 'nct_id')
