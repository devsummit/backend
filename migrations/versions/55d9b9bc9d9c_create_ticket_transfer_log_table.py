"""create ticket_transfer_log table

Revision ID: 55d9b9bc9d9c
Revises: 3ae3a27a9771
Create Date: 2017-08-07 09:44:36.568348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55d9b9bc9d9c'
down_revision = '3ae3a27a9771'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('ticket_transfer_log',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('ticket_id', sa.Integer, sa.ForeignKey('tickets.id')),
		sa.Column('sender_user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('receiver_user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
	op.drop_table('ticket_transfer_log')
