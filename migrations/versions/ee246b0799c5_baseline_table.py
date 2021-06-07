"""baseline table

Revision ID: ee246b0799c5
Revises: 3925cb73a63a
Create Date: 2021-06-06 14:50:10.117318

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = 'ee246b0799c5'
down_revision = '3925cb73a63a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('baselines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('base', sa.String(length=100), nullable=True),
    sa.Column('clss', sa.String(length=100), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('param_type', ENUM('MEAN', 'NUMBER', 'COUNT_OF_PARTICIPANTS', 'LEAST_SQUARES_MEAN', 'GEOMETRIC_MEAN', 'COUNT_OF_UNITS', 'GEOMETRIC_LEAST_SQUARES_MEAN', 'LOG_MEAN', 'NA', name='measure_param', create_type=False), nullable=True),
    sa.Column('dispersion', ENUM('STANDARD_DEVIATION', 'CONFIDENCE_INTERVAL_95', 'STANDARD_ERROR', 'FULL_RANGE', 'GEOMETRIC_COEFFICIENT_OF_VARIATION', 'INTER_QUARTILE_RANGE', 'CONFIDENCE_INTERVAL_90', 'CONFIDENCE_INTERVAL_80', 'CONFIDENCE_INTERVAL_97', 'CONFIDENCE_INTERVAL_99', 'CONFIDENCE_INTERVAL_60', 'CONFIDENCE_INTERVAL_96', 'CONFIDENCE_INTERVAL_98', 'CONFIDENCE_INTERVAL_70', 'CONFIDENCE_INTERVAL_85', 'CONFIDENCE_INTERVAL_75', 'CONFIDENCE_INTERVAL_94', 'CONFIDENCE_INTERVAL_100', 'NA', name='dispersion_param', create_type=False), nullable=True),
    sa.Column('unit', sa.String(length=40), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('spread', sa.Float(), nullable=True),
    sa.Column('upper', sa.Float(), nullable=True),
    sa.Column('type', sa.Enum('RACE', 'GENDER', 'ETHNICITY', 'AGE', 'OTHER', name='baseline_type'), nullable=True),
    sa.Column('sub_type', sa.Enum('WHITE', 'BLACK', 'ASIAN', 'INDIAN', 'PACIFIC', 'MALE', 'FEMALE', 'NA', name='baseline_subtype'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('baselines')
    op.execute('DROP TYPE baseline_subtype')
    op.execute('DROP TYPE baseline_type')
    # ### end Alembic commands ###
