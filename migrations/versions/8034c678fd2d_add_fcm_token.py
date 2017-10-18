"""add fcm token


Revision ID: 8034c678fd2d
Revises: 3967d0f62652
Create Date: 2017-09-20 18:07:16.193514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8034c678fd2d'
down_revision = '3967d0f62652'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('fcmtoken', sa.String(255)))
    


def downgrade():
    op.drop_column('users', 'fcmtoken')
