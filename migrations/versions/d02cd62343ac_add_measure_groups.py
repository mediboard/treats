"""add measure groups

Revision ID: d02cd62343ac
Revises: 398d4fd72f59
Create Date: 2022-08-20 22:18:02.933901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd02cd62343ac'
down_revision = '398d4fd72f59'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('measure_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('conditions', 'no_studies')
    op.add_column('measures', sa.Column('measureGroup', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'measures', 'measure_groups', ['measureGroup'], ['id'])


def downgrade():
    op.drop_constraint(None, 'measures', type_='foreignkey')
    op.drop_column('measures', 'measureGroup')
    op.add_column('conditions', sa.Column('no_studies', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_table('measure_groups')
