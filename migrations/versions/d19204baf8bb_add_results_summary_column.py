"""add results summary column

Revision ID: d19204baf8bb
Revises: b2edc4f164ee
Create Date: 2022-10-21 16:37:19.362518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd19204baf8bb'
down_revision = 'b2edc4f164ee'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('studies', sa.Column('results_summary', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('studies', 'results_summary')
