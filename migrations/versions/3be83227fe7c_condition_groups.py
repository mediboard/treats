"""condition_groups

Revision ID: 3be83227fe7c
Revises: 0dcc07737017
Create Date: 2022-09-26 10:36:31.496753

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3be83227fe7c'
down_revision = '0dcc07737017'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('condition_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=400), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('conditions', sa.Column('conditionGroup', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'conditions', 'condition_groups', ['conditionGroup'], ['id'])


def downgrade():
    op.drop_table('condition_groups')
