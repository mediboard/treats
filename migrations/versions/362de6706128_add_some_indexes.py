"""add some indexes

Revision ID: 362de6706128
Revises: 2fa83af62d6f
Create Date: 2023-03-08 16:48:04.480578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '362de6706128'
down_revision = '2fa83af62d6f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_baselines_study'), 'baselines', ['study'], unique=False)
    op.create_index(op.f('ix_effects_study'), 'effects', ['study'], unique=False)
    op.create_index(op.f('ix_study_conditions_condition'), 'study_conditions', ['condition'], unique=False)
    op.create_index(op.f('ix_study_conditions_study'), 'study_conditions', ['study'], unique=False)
    op.create_index(op.f('ix_study_treatments_study'), 'study_treatments', ['study'], unique=False)
    op.create_index(op.f('ix_study_treatments_treatment'), 'study_treatments', ['treatment'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_study_treatments_treatment'), table_name='study_treatments')
    op.drop_index(op.f('ix_study_treatments_study'), table_name='study_treatments')
    op.drop_index(op.f('ix_study_conditions_study'), table_name='study_conditions')
    op.drop_index(op.f('ix_study_conditions_condition'), table_name='study_conditions')
    op.drop_index(op.f('ix_effects_study'), table_name='effects')
    op.drop_index(op.f('ix_baselines_study'), table_name='baselines')
