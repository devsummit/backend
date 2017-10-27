"""add quota to discount referal

Revision ID: 47d9c68393ed
Revises: 2cd1143be61c
Create Date: 2017-10-27 10:02:21.976629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47d9c68393ed'
down_revision = '2cd1143be61c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('referals', sa.Column('quota', sa.Integer))


def downgrade():
    op.drop_column('referals', 'quota')
