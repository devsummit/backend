"""create partner-pj table

Revision ID: 2004f48169b4
Revises: 02d6f4f8cfe0
Create Date: 2017-10-31 14:29:25.286963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2004f48169b4'
down_revision = '02d6f4f8cfe0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'partner_pj',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('partner_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.drop_table('partner_pj')
