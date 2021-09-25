"""add no_studies to condition

Revision ID: 398d4fd72f59
Revises: 30cbe5f35678
Create Date: 2021-09-25 08:15:02.793027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '398d4fd72f59'
down_revision = '30cbe5f35678'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('conditions', sa.Column('no_studies', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('conditions', 'no_studies')
