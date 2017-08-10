"""create user_ticket table
Revision ID: 6cdc598b190b
Revises: 0db2d38988c5
Create Date: 2017-08-07 09:38:25.172824
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cdc598b190b'
down_revision = '0db2d38988c5'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('user_tickets',
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
                 sa.Column('ticket_id', sa.Integer,
                           sa.ForeignKey('tickets.id')),
                 sa.Column('created_at', sa.DateTime),
                 sa.Column('updated_at', sa.DateTime),
                 )


def downgrade():
	op.drop_table('user_tickets')
