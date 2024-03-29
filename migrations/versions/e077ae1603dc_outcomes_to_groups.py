"""outcomes to groups

Revision ID: e077ae1603dc
Revises: cda171c05194
Create Date: 2021-06-25 08:47:56.864575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e077ae1603dc'
down_revision = 'cda171c05194'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('outcomes', sa.Column('group', sa.Integer(), nullable=True))
    op.drop_constraint('outcomes_administration_fkey', 'outcomes', type_='foreignkey')
    op.create_foreign_key(None, 'outcomes', 'groups', ['group'], ['id'])
    op.drop_column('outcomes', 'administration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('outcomes', sa.Column('administration', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'outcomes', type_='foreignkey')
    op.create_foreign_key('outcomes_administration_fkey', 'outcomes', 'administrations', ['administration'], ['id'])
    op.drop_column('outcomes', 'group')
    # ### end Alembic commands ###
