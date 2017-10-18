"""add deleted_at field to feeds table

Revision ID: 0ed8801fa88a
Revises: b1dfd323d88f
Create Date: 2017-10-03 12:43:47.960140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ed8801fa88a'
down_revision = 'b1dfd323d88f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('feeds', sa.Column('deleted_at', sa.DateTime))


def downgrade():
    op.drop_column('feeds', 'deleted_at')
