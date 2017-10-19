"""add referer

Revision ID: 9b440795da0e
Revises: f030c3932db4
Create Date: 2017-10-19 19:30:29.048391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b440795da0e'
down_revision = 'f030c3932db4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('referer', sa.String(40)))


def downgrade():
    op.drop_column('users', 'referer')
