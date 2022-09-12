"""add measure group

Revision ID: a0b22bba7ecd
Revises: b9dd41e3e79c
Create Date: 2022-09-06 11:45:19.196981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0b22bba7ecd'
down_revision = 'b9dd41e3e79c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('effects_cluster',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('effects', sa.Column('cluster', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'effects', 'effects_cluster', ['cluster'], ['id'])


def downgrade():
    op.drop_constraint(None, 'effects', type_='foreignkey')
    op.drop_column('effects', 'cluster')
    op.drop_table('effects_cluster')
