"""edit_materials_table

Revision ID: 4a97ebacb049
Revises: caa004f8af83
Create Date: 2017-09-19 13:31:30.689961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a97ebacb049'
down_revision = 'caa004f8af83'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'materials',
         sa.Column('is_used', sa.Boolean(), server_default=sa.schema.DefaultClause("0"), 
         nullable=False)
    )


def downgrade():
    op.drop_column('materials', 'is_used')
