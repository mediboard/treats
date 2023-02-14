"""add study to effect group

Revision ID: 40e680708fa1
Revises: 23050104ac39
Create Date: 2022-09-12 14:15:57.992014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40e680708fa1'
down_revision = '23050104ac39'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('effectsgroups', sa.Column('study', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'effectsgroups', 'studies', ['study'], ['id'])
    op.create_index('effectsgroups_study_ind', 'effectsgroups', ['study'], unique=False)
    op.create_index('effects_study_ind', 'effects', ['study'], unique=False)
    op.create_index('effects_group_ind', 'effects', ['group'], unique=False)


def downgrade():
    op.drop_constraint(None, 'effectsgroups', type_='foreignkey')
    op.drop_column('effectsgroups', 'study')
    op.drop_index('effectsgroups_study_ind')
    op.drop_index('effects_study_ind')
    op.drop_index('effects_group_ind')
