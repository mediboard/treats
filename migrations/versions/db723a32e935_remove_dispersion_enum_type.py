"""remove dispersion enum type

Revision ID: db723a32e935
Revises: 5ab7eac4b63b
Create Date: 2023-02-14 13:51:54.144075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db723a32e935'
down_revision = '5ab7eac4b63b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('measures', 'dispersion', type_=sa.String(length=50))
    op.alter_column('baselines', 'dispersion', type_=sa.String(length=50))


def downgrade():
    print("who cares")
