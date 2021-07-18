"""adds effect type

Revision ID: b8254aff553a
Revises: 59d3e74e88fa
Create Date: 2021-07-18 11:32:27.550826

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b8254aff553a'
down_revision = '59d3e74e88fa'
branch_labels = None
depends_on = None


def upgrade():
    effect_type = postgresql.ENUM('SERIOUS', 'OTHER', name='effect_type')
    effect_type.create(op.get_bind())

    op.add_column('effects', sa.Column('effect_type', sa.Enum('SERIOUS', 'OTHER', name='effect_type'), nullable=True))


def downgrade():
    op.drop_column('effects', 'effect_type')
    op.execute("DROP TYPE effect_type")
