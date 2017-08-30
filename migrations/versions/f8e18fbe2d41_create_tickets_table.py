"""create tickets table
Revision ID: f8e18fbe2d41
Revises: 79d78e481ff5
Create Date: 2017-08-01 19:23:29.919062
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8e18fbe2d41'
down_revision = '79d78e481ff5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ticket_type', sa.String, unique=True),
        sa.Column('price', sa.Float),
        sa.Column('information', sa.String),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('tickets')
