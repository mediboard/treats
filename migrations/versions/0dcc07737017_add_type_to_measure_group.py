"""add type to measure group

Revision ID: 0dcc07737017
Revises: 9a849ffa6fa2
Create Date: 2022-09-15 11:58:30.086489

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '0dcc07737017'
down_revision = '9a849ffa6fa2'
branch_labels = None
depends_on = None


def upgrade():
    measure_group_type = postgresql.ENUM('PRIMARY', 'SECONDARY', 'OTHER', 'IRRELEVANT', name='measure_group_type')
    measure_group_type.create(op.get_bind())
    op.add_column('measure_groups', sa.Column('type', sa.Enum('PRIMARY', 'SECONDARY', 'OTHER', 'IRRELEVANT', name='measure_group_type'), nullable=True))


def downgrade():
    op.drop_column('measure_groups', 'type')
