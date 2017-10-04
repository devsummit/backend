"""create_prize_lists_table

Revision ID: 90062c172360
Revises: 0871ffb7defd
Create Date: 2017-10-03 17:57:44.084132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90062c172360'
down_revision = '0871ffb7defd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'prize_lists',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('point_cost', sa.Integer),
        sa.Column('name', sa.String(120)),
        sa.Column('attachment', sa.String(255)),
        sa.Column('count', sa.Integer),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('prize_lists')
