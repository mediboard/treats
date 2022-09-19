"""add condition to measure groups

Revision ID: 2732841ad3e4
Revises: 40e680708fa1
Create Date: 2022-09-14 08:19:32.812282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2732841ad3e4'
down_revision = '40e680708fa1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('measure_groups', sa.Column('condition', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'measure_groups', 'conditions', ['condition'], ['id'])
    op.create_index('measure_groups_condition_ind', 'measure_groups', ['condition'], unique=False)


def downgrade():
    op.drop_constraint(None, 'measure_groups', type_='foreignkey')
    op.drop_column('measure_groups', 'condition')
    op.drop_index('measure_groups_condition_ind', table_name='measure_groups')
