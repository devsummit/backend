"""add curency to payments table

Revision ID: d40a0bb48635
Revises: efe85d220dc5, e1d00374aede, 14bd1c1fb1d2
Create Date: 2017-10-13 20:21:30.497503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd40a0bb48635'
down_revision = ('efe85d220dc5', 'e1d00374aede', '14bd1c1fb1d2')
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('payments', sa.Column('currency', sa.String(255)))


def downgrade():
    op.drop_column('payments', 'currency')
