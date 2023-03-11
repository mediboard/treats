"""add search

Revision ID: 6171b5913fda
Revises: 362de6706128
Create Date: 2023-03-11 08:40:59.505345

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6171b5913fda'
down_revision = '362de6706128'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('searches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=300), nullable=False),
        sa.Column('search_string', sa.String(length=2000), nullable=True),
        sa.Column('original_user', sa.String(length=1000), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_searches_original_user'), 'searches', ['original_user'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_searches_original_user'), table_name='searches')
    op.drop_table('searches')
