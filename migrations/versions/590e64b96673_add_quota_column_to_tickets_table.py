"""add_quota_column_to_tickets_table

Revision ID: 590e64b96673
Revises: e24020fea140
Create Date: 2017-10-16 23:02:21.686634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '590e64b96673'
down_revision = 'e24020fea140'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tickets', sa.Column('quota', sa.Integer))


def downgrade():
    op.drop_column('tickets', 'quota')