"""add annotated to groups

Revision ID: 3055b7729b26
Revises: cd69847bbd25
Create Date: 2022-12-26 14:24:19.505367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3055b7729b26'
down_revision = 'cd69847bbd25'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('groups', sa.Column('annotated', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('groups', 'annotated')
