"""create referal table

Revision ID: f40fd4fc554d
Revises: 82e92967c0cd
Create Date: 2017-09-04 23:56:29.716268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f40fd4fc554d'
down_revision = 'f8e18fbe2d41'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'referals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner', sa.String(255)),
        sa.Column('discount_amount', sa.Float(precision=2)),
        sa.Column('referal_code', sa.String(120)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.drop_table('referals')
