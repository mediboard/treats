"""add no results study fields

Revision ID: f7ebf4bea8e3
Revises: da8645cc476f
Create Date: 2023-02-14 12:53:33.632428

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'f7ebf4bea8e3'
down_revision = 'da8645cc476f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('studies', sa.Column('stopped_reason', sa.String(length=251), nullable=True))

    study_status = postgresql.ENUM('PRE_RECRUITING', 'RECRUITING', 'ENROLLING', 'ACTIVE', 'COMPLETED', 'SUSPENDED', 'TERMINATED', 'WITHDRAWN', name='study_status')
    study_status.create(op.get_bind())

    op.add_column('studies', sa.Column('status', sa.Enum('PRE_RECRUITING', 'RECRUITING', 'ENROLLING', 'ACTIVE', 'COMPLETED', 'SUSPENDED', 'TERMINATED', 'WITHDRAWN', name='study_status'), nullable=True))


def downgrade():
    op.drop_column('studies', 'status')
    op.drop_column('studies', 'stopped_reason')
