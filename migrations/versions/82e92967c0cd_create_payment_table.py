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
            sa.Column('card_id', sa.Integer),
            sa.Column('total', sa.Integer),
            sa.Column('additional_information', sa.Text),
            sa.Column('sender', sa.String),
            sa.Column('order_id', sa.Integer, sa.ForeignKey('order.id')),
            sa.Column('created_at', sa.DateTime),
            sa.Column('updated_at', sa.DateTime),
    )


def downgrade():
    op.drop_table('payments')
