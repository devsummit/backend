"""create_order_verifications_table

Revision ID: 14bd1c1fb1d2
Revises: b186f6b143e0
Create Date: 2017-10-13 16:48:19.527441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14bd1c1fb1d2'
down_revision = 'b186f6b143e0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('order_verifications',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('order_id', sa.String(180), sa.ForeignKey('orders.id')),
		sa.Column('payment_proof', sa.String(255)),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime)
		)

def downgrade():
    op.drop_table('order_verifications')
