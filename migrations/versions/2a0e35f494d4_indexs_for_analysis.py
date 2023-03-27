"""indexs for analysis

Revision ID: 2a0e35f494d4
Revises: f18ef4aaae62
Create Date: 2023-03-27 15:44:12.871077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a0e35f494d4'
down_revision = 'f18ef4aaae62'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_administrations_group'), 'administrations', ['group'], unique=False)
    op.create_index(op.f('ix_administrations_treatment'), 'administrations', ['treatment'], unique=False)
    op.create_index(op.f('ix_measure_group_measures_measure'), 'measure_group_measures', ['measure'], unique=False)
    op.create_index(op.f('ix_measure_group_measures_measureGroup'), 'measure_group_measures', ['measureGroup'], unique=False)
    op.create_index(op.f('ix_measures_study'), 'measures', ['study'], unique=False)
    op.create_index(op.f('ix_outcomes_group'), 'outcomes', ['group'], unique=False)
    op.create_index(op.f('ix_outcomes_measure'), 'outcomes', ['measure'], unique=False)
    op.create_index(op.f('ix_outcomes_study'), 'outcomes', ['study'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_outcomes_study'), table_name='outcomes')
    op.drop_index(op.f('ix_outcomes_measure'), table_name='outcomes')
    op.drop_index(op.f('ix_outcomes_group'), table_name='outcomes')
    op.drop_index(op.f('ix_measures_study'), table_name='measures')
    op.drop_index(op.f('ix_measure_group_measures_measureGroup'), table_name='measure_group_measures')
    op.drop_index(op.f('ix_measure_group_measures_measure'), table_name='measure_group_measures')
    op.drop_index(op.f('ix_administrations_treatment'), table_name='administrations')
    op.drop_index(op.f('ix_administrations_group'), table_name='administrations')
