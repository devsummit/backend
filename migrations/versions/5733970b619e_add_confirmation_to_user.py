"""add confirmation to user

Revision ID: 5733970b619e
Revises: 66237493cf86
Create Date: 2017-10-18 21:05:43.815517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5733970b619e'
down_revision = '66237493cf86'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('confirmed', sa.DateTime))


def downgrade():
    op.drop_column('users', 'confirmed')
