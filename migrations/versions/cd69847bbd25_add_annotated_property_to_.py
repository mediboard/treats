"""add annotated property to administrations

Revision ID: cd69847bbd25
Revises: f4f1a3bfec7f
Create Date: 2022-12-20 16:02:58.929463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd69847bbd25'
down_revision = 'f4f1a3bfec7f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('administrations', sa.Column('annotated', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('administrations', 'annotated')
