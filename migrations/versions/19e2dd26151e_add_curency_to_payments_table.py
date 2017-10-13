"""add curency to payments table

Revision ID: 19e2dd26151e
Revises: efe85d220dc5, e1d00374aede
Create Date: 2017-10-13 19:31:42.719437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19e2dd26151e'
down_revision = ('efe85d220dc5', 'e1d00374aede')
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('payments', sa.Column('currency', sa.String(255)))


def downgrade():
    op.drop_column('payments', 'currency')
