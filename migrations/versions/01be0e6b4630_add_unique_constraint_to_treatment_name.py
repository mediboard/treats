"""add unique constraint to treatment name

Revision ID: 01be0e6b4630
Revises: 1f8cb793f08f
Create Date: 2023-01-31 07:16:37.238157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01be0e6b4630'
down_revision = '1f8cb793f08f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'treatments', ['name'])


def downgrade():
    op.drop_constraint(None, 'treatments', type_='unique')
