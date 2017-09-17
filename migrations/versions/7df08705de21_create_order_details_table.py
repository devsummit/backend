"""create order_details table

Revision ID: 7df08705de21
Revises: 05cb70b1d87c
Create Date: 2017-08-01 19:23:56.545130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7df08705de21'
down_revision = '05cb70b1d87c'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'order_details',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('ticket_id', sa.Integer,
		sa.ForeignKey('tickets.id')),
		sa.Column('order_id', sa.String(180),
			sa.ForeignKey('orders.id')),
		sa.Column('count', sa.Integer),
		sa.Column('price', sa.Integer),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime)
		)


def downgrade():
	op.drop_table('order_details')
