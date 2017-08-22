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
            sa.Column('order_id', sa.Integer, sa.ForeignKey('order.id')),
            sa.Column('saved_token_id', sa.Integer),
            sa.Column('transaction_id', sa.Integer),
            sa.Column('midtrans_order_id', sa.Integer),
            sa.Column('payment_type', sa.String),
            sa.Column('gross_amount', sa.Integer),
            sa.Column('transaction_time', sa.String),
            sa.Column('transaction_status', sa.String),
            sa.Column('masked_card', sa.String),
            sa.Column('bank', sa.String),
            sa.Column('fraud_status', sa.String),
            sa.Column('created_at', sa.DateTime),
            sa.Column('updated_at', sa.DateTime),
    )


def downgrade():
    op.drop_table('payments')
