"""add NA to stuy_type

Revision ID: 5ab7eac4b63b
Revises: f7ebf4bea8e3
Create Date: 2023-02-14 13:16:04.987042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ab7eac4b63b'
down_revision = 'f7ebf4bea8e3'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE study_type ADD VALUE 'NA'")

def downgrade():
    op.execute("ALTER TYPE study_type DROP VALUE 'NA'")
