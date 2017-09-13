"""create_entry_cash

Revision ID: ae0efd1cf5c1
Revises: f66e7f85d4e7
Create Date: 2017-09-11 20:22:28.379213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae0efd1cf5c1'
down_revision = 'f66e7f85d4e7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('entry_cash_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('amount', sa.Integer),
        sa.Column('description', sa.String(120)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )


def downgrade():
    op.drop_table('entry_cash_log')
