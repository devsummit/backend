"""add referer column user table

Revision ID: caa004f8af83
Revises: 77e953519a64
Create Date: 2017-09-18 17:51:43.284235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'caa004f8af83'
down_revision = '77e953519a64'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('referer', sa.String(40)))


def downgrade():
    op.add_column('users', 'referer')
