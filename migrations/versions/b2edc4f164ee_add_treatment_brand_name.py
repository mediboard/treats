"""add treatment brand name

Revision ID: b2edc4f164ee
Revises: 5201b1561ec1
Create Date: 2022-10-13 16:31:23.948780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2edc4f164ee'
down_revision = '5201b1561ec1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('treatment_brand_names',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('treatment', sa.Integer(), nullable=True),
    sa.Column('brand_name', sa.String(length=400), nullable=True),
    sa.ForeignKeyConstraint(['treatment'], ['treatments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'study_treatments', 'treatments', ['treatment'], ['id'])
    op.create_foreign_key(None, 'study_treatments', 'studies', ['study'], ['id'])


def downgrade():
    op.drop_constraint(None, 'study_treatments', type_='foreignkey')
    op.drop_constraint(None, 'study_treatments', type_='foreignkey')
    op.create_index('study_treatments_study_ind', 'study_treatments', ['study'], unique=False)
    op.drop_table('treatment_brand_names')
