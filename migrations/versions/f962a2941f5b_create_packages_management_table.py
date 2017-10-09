"""create_packages_management_table

Revision ID: f962a2941f5b
Revises: 063911936966
Create Date: 2017-10-09 11:41:42.259094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f962a2941f5b'
down_revision = '063911936966'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('packages_management',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('name', sa.String(255)),
		sa.Column('price', sa.Numeric(12, 2)),
		sa.Column('quota', sa.Integer),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime)
		)

def downgrade():
    op.drop_table('packages_management')
