"""pipelines fix

Revision ID: 19889d69f95d
Revises: fe919adc35a7
Create Date: 2023-02-10 12:06:29.148651

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '19889d69f95d'
down_revision = 'fe919adc35a7'
branch_labels = None
depends_on = None


def upgrade():
    phase_type = postgresql.ENUM('NA', 'EARLY_PHASE_1', 'PHASE_1', 'PHASE_1_PHASE_2', 'PHASE_2', 'PHASE_2_PHASE_3', 'PHASE_3', 'PHASE_4', name='phase_type')
    phase_type.create(op.get_bind())

    op.add_column('comparison', sa.Column('group', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comparison', 'groups', ['group'], ['id'])
    op.create_foreign_key(None, 'effects', 'effectsgroups', ['group'], ['id'])
    op.add_column('studies', sa.Column('phase', sa.Enum('NA', 'EARLY_PHASE_1', 'PHASE_1', 'PHASE_1_PHASE_2', 'PHASE_2', 'PHASE_2_PHASE_3', 'PHASE_3', 'PHASE_4', name='phase_type'), nullable=True))


def downgrade():
    op.drop_column('studies', 'phase')
