"""treatment diffs

Revision ID: 9e27780f09a6
Revises: 3055b7729b26
Create Date: 2023-01-15 09:39:29.070868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e27780f09a6'
down_revision = '3055b7729b26'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('group_pairs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_a', sa.Integer(), nullable=True),
    sa.Column('group_b', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_a'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['group_b'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('treatment_diffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('condition', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['condition'], ['conditions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('base_treatments_diffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('treatment_diff', sa.Integer(), nullable=True),
    sa.Column('treatment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['treatment'], ['treatments.id'], ),
    sa.ForeignKeyConstraint(['treatment_diff'], ['treatment_diffs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('diff_treatments_diffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('treatment_diff', sa.Integer(), nullable=True),
    sa.Column('treatment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['treatment'], ['treatments.id'], ),
    sa.ForeignKeyConstraint(['treatment_diff'], ['treatment_diffs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('group_pair_diffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_pair', sa.Integer(), nullable=True),
    sa.Column('treatment_diff', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_pair'], ['group_pairs.id'], ),
    sa.ForeignKeyConstraint(['treatment_diff'], ['treatment_diffs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index('diff_treatments_diffs_treatment_diffs', 'diff_treatments_diffs', ['treatment_diff'], unique=False)
    op.create_index('diff_treatments_diffs_treatments', 'diff_treatments_diffs', ['treatment'], unique=False)

    op.create_index('base_treatments_diffs_treatment_diffs', 'base_treatments_diffs', ['treatment_diff'], unique=False)
    op.create_index('base_treatments_diffs_treatments', 'base_treatments_diffs', ['treatment'], unique=False)

    op.create_index('group_pairs_a_groups', 'group_pairs', ['group_a'], unique=False)
    op.create_index('group_pairs_b_groups', 'group_pairs', ['group_b'], unique=False)

    op.create_index('group_pair_diffs_group_pairs', 'group_pair_diffs', ['group_pair'], unique=False)
    op.create_index('group_pair_diffs_treatment_diffs', 'group_pair_diffs', ['treatment_diff'], unique=False)


def downgrade():
    op.drop_table('group_pair_diffs')
    op.drop_table('diff_treatments_diffs')
    op.drop_table('base_treatments_diffs')
    op.drop_table('treatment_diffs')
    op.drop_table('group_pairs')
