"""adds direct study conditions

Revision ID: 30cbe5f35678
Revises: ae353ca2586b
Create Date: 2021-08-22 08:34:04.054630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30cbe5f35678'
down_revision = 'ae353ca2586b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('study_treatments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('study', sa.Integer(), nullable=True),
    sa.Column('treatment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['study'], ['studies.id'], ),
    sa.ForeignKeyConstraint(['treatment'], ['treatments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('study_treatments')
    # ### end Alembic commands ###
