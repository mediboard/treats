"""add treatment group

Revision ID: b9dd41e3e79c
Revises: d02cd62343ac
Create Date: 2022-09-06 10:23:30.231644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9dd41e3e79c'
down_revision = 'd02cd62343ac'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('treatment_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=400), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('treatments', sa.Column('treatmentGroup', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'treatments', 'treatment_groups', ['treatmentGroup'], ['id'])


def downgrade():
    op.drop_constraint(None, 'treatments', type_='foreignkey')
    op.drop_column('treatments', 'treatmentGroup')
    op.drop_table('treatment_groups')
