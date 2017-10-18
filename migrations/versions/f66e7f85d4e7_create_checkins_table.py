"""create checkins table

Revision ID: f66e7f85d4e7
Revises: 979820a6fae2
Create Date: 2017-09-04 23:57:37.500025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f66e7f85d4e7'
down_revision = '82e92967c0cd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'check_ins',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_ticket_id', sa.Integer,
            sa.ForeignKey('user_tickets.id')),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.drop_table('check_ins')
