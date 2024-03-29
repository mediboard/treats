"""condition_groups_v2

Revision ID: 7e80bb3959b6
Revises: 3be83227fe7c
Create Date: 2022-09-26 13:42:24.068259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e80bb3959b6'
down_revision = '3be83227fe7c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('conditions', sa.Column('condition_group', sa.Integer(), nullable=True))
    op.drop_constraint('conditions_conditionGroup_fkey', 'conditions', type_='foreignkey')
    op.create_foreign_key(None, 'conditions', 'condition_groups', ['condition_group'], ['id'])
    op.drop_column('conditions', 'conditionGroup')


def downgrade():
    op.add_column('conditions', sa.Column('conditionGroup', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'conditions', type_='foreignkey')
    op.create_foreign_key('conditions_conditionGroup_fkey', 'conditions', 'condition_groups', ['conditionGroup'], ['id'])
    op.drop_index(op.f('ix_conditions_name'), table_name='conditions')
    op.drop_column('conditions', 'condition_group')
