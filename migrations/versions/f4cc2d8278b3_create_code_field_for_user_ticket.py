"""create code field for user_ticket

Revision ID: f4cc2d8278b3
Revises: 8abc4815e14a, 8034c678fd2d
Create Date: 2017-09-25 20:21:40.251115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4cc2d8278b3'
down_revision = ('8abc4815e14a', '8034c678fd2d')
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user_tickets', sa.Column('ticket_code', sa.String(255)))


def downgrade():
    op.drop_column('user_tickets', 'ticket_code')

