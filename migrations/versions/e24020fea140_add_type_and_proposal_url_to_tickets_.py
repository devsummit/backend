"""add type and proposal_url to tickets table

Revision ID: e24020fea140
Revises: 2ab819f84611
Create Date: 2017-10-16 21:28:12.043093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e24020fea140'
down_revision = '2ab819f84611'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tickets', sa.Column('type', sa.String(255)))
    op.add_column('tickets', sa.Column('proposal_url', sa.String(255)))


def downgrade():
    op.drop_column('tickets', 'type')
    op.drop_column('tickets', 'proposal_url')
