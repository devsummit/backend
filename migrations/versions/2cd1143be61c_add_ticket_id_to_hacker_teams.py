"""add ticket_id to hacker_teams

Revision ID: 2cd1143be61c
Revises: 88c366de3537, 9b440795da0e
Create Date: 2017-10-20 17:27:42.154128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cd1143be61c'
down_revision = ('88c366de3537', '9b440795da0e')
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('hacker_teams', sa.Column('ticket_id', sa.Integer))


def downgrade():
    op.drop_column('hacker_teams', sa.Column('ticket_id', sa.Integer))
