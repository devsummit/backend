"""create order table

Revision ID: 05cb70b1d87c
Revises: f8e18fbe2d41
Create Date: 2017-08-01 19:23:51.523518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05cb70b1d87c'
down_revision = 'f8e18fbe2d41'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer,
            sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('status', sa.String),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.drop_table('orders')

