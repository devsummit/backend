"""create payment table

Revision ID: 82e92967c0cd
Revises: d0f006ed40b0
Create Date: 2017-08-22 14:37:45.385524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82e92967c0cd'
down_revision = 'd0f006ed40b0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
            'payments',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id')),
            sa.Column('saved_token_id', sa.String(255)),
            sa.Column('transaction_id', sa.String(255)),
            sa.Column('payment_type', sa.String(120)),
            sa.Column('gross_amount', sa.Integer),
            sa.Column('transaction_time', sa.DateTime),
            sa.Column('transaction_status', sa.String(120)),
            sa.Column('masked_card', sa.String(255)),
            sa.Column('bank', sa.String(120)),
            sa.Column('fraud_status', sa.String(120)),
            sa.Column('va_number', sa.String(120)),
            sa.Column('created_at', sa.DateTime),
            sa.Column('updated_at', sa.DateTime),
            sa.Column('expired_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('payments')
