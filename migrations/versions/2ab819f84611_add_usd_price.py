"""add usd price

Revision ID: 2ab819f84611
Revises: 98ecbda34ad3
Create Date: 2017-10-14 05:19:36.287325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ab819f84611'
down_revision = '98ecbda34ad3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tickets', sa.Column('usd_price', sa.Integer))


def downgrade():
    op.drop_column('tickets', 'usd_price')
