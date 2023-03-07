"""add study design feilds

Revision ID: 2fa83af62d6f
Revises: d2c1241d1003
Create Date: 2023-03-07 08:40:47.405668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fa83af62d6f'
down_revision = 'd2c1241d1003'
branch_labels = None
depends_on = None


def upgrade():
    design_allocation_type = sa.Enum('RANDOMIZED', 'NON_RANDOMIZED', 'NA', name='design_allocation')
    design_allocation_type.create(op.get_bind())
    op.add_column('studies', sa.Column('design_allocation', design_allocation_type, nullable=True))

    design_masking_type = sa.Enum('NONE', 'SINGLE', 'DOUBLE', 'QUADRUPLE', 'TRIPLE', 'NA', name='design_masking')
    design_masking_type.create(op.get_bind())
    op.add_column('studies', sa.Column('design_masking', design_masking_type, nullable=True))

    design_time_perspective_type = sa.Enum('PROSPECTIVE', 'RETROSPECTIVE', 'CROSS_SECTIONAL', 'OTHER', 'NA', name='design_time_perspective')
    design_time_perspective_type.create(op.get_bind())
    op.add_column('studies', sa.Column('design_time_perspective', design_time_perspective_type, nullable=True))

    who_masked_type = sa.Enum('PARTICIPANT', 'INVESTIGATOR', 'OUTCOMES_ASSESSOR', 'CARE_PROVIDER', 'NA', name='who_masked')
    who_masked_type.create(op.get_bind())
    op.add_column('studies', sa.Column('who_masked', sa.ARRAY(who_masked_type), nullable=True))

    observational_model_type = sa.Enum('COHORT', 'CASE_CONTROL', 'CASE_ONLY', 'OTHER', 'ECOLOGIC_OR_COMMUNITY', 'CASE_CROSSOVER', 'DEFINED_POPULATION', 'FAMILY_BASED', 'NATURAL_HISTORY', 'NA', name='observational_model')
    observational_model_type.create(op.get_bind())
    op.add_column('studies', sa.Column('observational_model', observational_model_type, nullable=True))
    op.add_column('studies', sa.Column('masking_description', sa.String(length=1200), nullable=True))
    op.add_column('studies', sa.Column('model_description', sa.String(length=1100), nullable=True))


def downgrade():
    op.drop_column('studies', 'model_description')
    op.drop_column('studies', 'masking_description')
    op.drop_column('studies', 'observational_model')
    op.drop_column('studies', 'who_masked')
    op.drop_column('studies', 'design_time_perspective')
    op.drop_column('studies', 'design_masking')
    op.drop_column('studies', 'design_allocation')
