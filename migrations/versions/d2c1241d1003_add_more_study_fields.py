"""add more study fields

Revision ID: d2c1241d1003
Revises: db723a32e935
Create Date: 2023-02-14 14:38:22.894288

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.models import study_status


# revision identifiers, used by Alembic.
revision = 'd2c1241d1003'
down_revision = 'db723a32e935'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE study_status ADD VALUE 'NOT_YET_RECRUITING'")
    op.execute("ALTER TYPE study_status ADD VALUE 'ACTIVE_NOT_RECRUITING'")
    op.execute("ALTER TYPE study_status ADD VALUE 'ENROLLING_BY_INVITATION'")
    op.execute("ALTER TYPE study_status ADD VALUE 'NO_LONGER_AVAILABLE'")
    op.execute("ALTER TYPE study_status ADD VALUE 'AVAILABLE'")
    op.execute("ALTER TYPE study_status ADD VALUE 'APPROVED_FOR_MARKETING'")
    op.execute("ALTER TYPE study_status ADD VALUE 'TEMPORARILY_NOT_AVAILABLE'")
    op.execute("ALTER TYPE study_status ADD VALUE 'UNKNOWN_STATUS'")
    op.execute("ALTER TYPE study_status ADD VALUE 'WITHHELD'")



    op.add_column('studies', sa.Column('completion_date', sa.Date(), nullable=True))


    completion_date_type = postgresql.ENUM('ACTUAL', 'ANTICIPATED', 'NA', name='completion_date_type')
    completion_date_type.create(op.get_bind())
    op.add_column('studies', sa.Column('completion_date_type', sa.Enum('ACTUAL', 'ANTICIPATED', 'NA', name='completion_date_type'), nullable=True))


def downgrade():
    op.drop_column('studies', 'completion_date_type')

    op.execute("DROP TYPE completion_date_type")

    op.drop_column('studies', 'completion_date')

    temp_enum = sa.Enum('PRE_RECRUITING', 'RECRUITING', 'ENROLLING', 'ACTIVE', 'COMPLETED', 'SUSPENDED', 'TERMINATED', 'WITHDRAWN', name="temp_enum")
    temp_enum.create(op.get_bind(), checkfirst=False)

    # Update the existing columns to use the new enum type
    op.execute("ALTER TABLE studies ALTER COLUMN status TYPE temp_enum USING status::text::temp_enum")

    # Drop the old enum type
    op.execute("DROP TYPE study_status")

    # Rename the temporary enum to the original name
    op.execute("ALTER TYPE temp_enum RENAME TO study_status")

