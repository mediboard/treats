"""make measure groups measures table

Revision ID: 9a849ffa6fa2
Revises: 2732841ad3e4
Create Date: 2022-09-14 10:48:46.161676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a849ffa6fa2'
down_revision = '2732841ad3e4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('measure_group_measures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measure', sa.Integer(), nullable=True),
    sa.Column('measureGroup', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['measure'], ['measures.id'], ),
    sa.ForeignKeyConstraint(['measureGroup'], ['measure_groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('measure_groups_condition_ind', table_name='measure_groups')
    op.drop_constraint('measures_measureGroup_fkey', 'measures', type_='foreignkey')
    op.drop_column('measures', 'measureGroup')


def downgrade():
    op.add_column('measures', sa.Column('measureGroup', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('measures_measureGroup_fkey', 'measures', 'measure_groups', ['measureGroup'], ['id'])
    op.create_index('measure_groups_condition_ind', 'measure_groups', ['condition'], unique=False)
    op.drop_table('measure_group_measures')
