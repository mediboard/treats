"""effects groups and admins

Revision ID: 59d3e74e88fa
Revises: e077ae1603dc
Create Date: 2021-07-16 08:32:17.443891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59d3e74e88fa'
down_revision = 'e077ae1603dc'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('effects_group_fkey', 'effects', type_='foreignkey')
    
    op.create_table('effectsgroups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=101), nullable=True),
    sa.Column('description', sa.String(length=1500), nullable=True),
    sa.Column('study_id', sa.String(length=7), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('effectsadministrations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group', sa.Integer(), nullable=True),
    sa.Column('treatment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group'], ['effectsgroups.id'], ),
    sa.ForeignKeyConstraint(['treatment'], ['treatments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('effectsadministrations')
    op.drop_table('effectsgroups')
