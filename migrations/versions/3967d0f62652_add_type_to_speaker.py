"""add type to speaker

Revision ID: 3967d0f62652
Revises: 0f1eecdee15c
Create Date: 2017-09-20 15:06:48.148631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3967d0f62652'
down_revision = '0f1eecdee15c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('speakers', sa.Column('type', sa.String(40)))


def downgrade():
    op.drop_column('speakers', 'type')
