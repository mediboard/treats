"""add insights

Revision ID: f4f1a3bfec7f
Revises: d19204baf8bb
Create Date: 2022-10-25 15:09:42.294739

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'f4f1a3bfec7f'
down_revision = 'd19204baf8bb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('insights',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('study', sa.String(length=11), nullable=True),
        sa.Column('measure', sa.Integer(), nullable=True),
        sa.Column('type', sa.Enum('STUDY', 'BASELINE', 'MEASURE', 'ADVERSE_EFFECT', name='insight_type'), nullable=True),
        sa.Column('body', sa.String(length=1000), nullable=True),
        sa.ForeignKeyConstraint(['measure'], ['measures.id'], ),
        sa.ForeignKeyConstraint(['study'], ['studies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('insights')
