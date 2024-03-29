"""condition scoring

Revision ID: 8fb586ba22b1
Revises: b8254aff553a
Create Date: 2021-07-31 12:33:03.383119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fb586ba22b1'
down_revision = 'b8254aff553a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('conditionscores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('treatment', sa.Integer(), nullable=True),
    sa.Column('condition', sa.Integer(), nullable=True),
    sa.Column('mixed_score', sa.Float(), nullable=True),
    sa.Column('singular_score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['condition'], ['conditions.id'], ),
    sa.ForeignKeyConstraint(['treatment'], ['treatments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint("uq_treatment_condition", "conditionscores", ['treatment', 'condition'])
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('conditionscores')
    # ### end Alembic commands ###
