"""adds precriptions to treatments

Revision ID: 5201b1561ec1
Revises: 7e80bb3959b6
Create Date: 2022-10-04 08:34:02.096499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5201b1561ec1'
down_revision = '7e80bb3959b6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('treatments', sa.Column('no_prescriptions', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('treatments', 'no_prescriptions')
