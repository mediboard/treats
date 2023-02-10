"""merging two heads

Revision ID: fe919adc35a7
Revises: 9e27780f09a6, 01be0e6b4630
Create Date: 2023-02-10 12:04:49.985708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe919adc35a7'
down_revision = ('9e27780f09a6', '01be0e6b4630')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
