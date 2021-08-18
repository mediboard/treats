"""add at risk to effects

Revision ID: ae353ca2586b
Revises: 8fb586ba22b1
Create Date: 2021-08-18 07:29:25.981165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae353ca2586b'
down_revision = '8fb586ba22b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('effects', sa.Column('no_at_risk', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    op.drop_column('effects', 'no_at_risk')
    # ### end Alembic commands ###
