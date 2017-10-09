"""create invoice table

Revision ID: 2ad9bae1b2c3
Revises: 063911936966
Create Date: 2017-10-09 14:07:38.156557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ad9bae1b2c3'
down_revision = '063911936966'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'invoices',
        sa.Column('id', sa.String(180), primary_key=True),
        sa.Column('invoiceable_id', sa.Integer),
        sa.Column('invoiceable_type', sa.String(120)),
        sa.Column('address', sa.String(255)),
        sa.Column('description', sa.String(255)),
        sa.Column('total', sa.Integer),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.drop_table('invoices')
