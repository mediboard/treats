"""add value to study purpose

Revision ID: 1f8cb793f08f
Revises: 3ba79366b8c6
Create Date: 2023-01-18 13:51:01.018143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f8cb793f08f'
down_revision = '3ba79366b8c6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE purpose ADD VALUE 'EDUCATIONAL_COUNSELING_TRAINING'")

def downgrade():
    op.execute("ALTER TYPE purpose DROP VALUE 'EDUCATIONAL_COUNSELING_TRAINING'")
