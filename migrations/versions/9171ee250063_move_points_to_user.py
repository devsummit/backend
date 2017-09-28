"""move points to user

Revision ID: 9171ee250063
Revises: 5cb51ff416bc, 3e0424b67645
Create Date: 2017-09-28 17:54:45.180936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9171ee250063'
down_revision = ('5cb51ff416bc', '3e0424b67645')
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('points', sa.Integer, default=0))


def downgrade():
    op.drop_column('users', 'points')
