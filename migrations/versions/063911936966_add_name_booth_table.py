"""add_name_booth_table

Revision ID: 063911936966
Revises: 7825659604b1
Create Date: 2017-10-06 16:02:15.563592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '063911936966'
down_revision = '7825659604b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('booths', sa.Column('name', sa.String(255)))


def downgrade():
    op.drop_column('booths', 'name')
