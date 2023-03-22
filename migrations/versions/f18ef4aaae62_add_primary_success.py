"""add primary success

Revision ID: f18ef4aaae62
Revises: 6171b5913fda
Create Date: 2023-03-21 16:59:14.324624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f18ef4aaae62'
down_revision = '6171b5913fda'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('studies', sa.Column('primary_success', sa.SmallInteger(), server_default='-1', nullable=False))


def downgrade():
    op.drop_column('studies', 'primary_success')
