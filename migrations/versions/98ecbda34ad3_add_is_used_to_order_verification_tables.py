"""add is_used to order_verification_tables

Revision ID: 98ecbda34ad3
Revises: d40a0bb48635
Create Date: 2017-10-14 00:21:19.861897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98ecbda34ad3'
down_revision = 'd40a0bb48635'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('order_verifications', sa.Column('is_used', sa.Integer))


def downgrade():
    op.drop_column('order_verifications', 'is_used')
