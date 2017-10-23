"""add_confirmed_field_to_users

Revision ID: f030c3932db4
Revises: 66237493cf86
Create Date: 2017-10-19 17:19:54.561812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f030c3932db4'
down_revision = '66237493cf86'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('confirmed', sa.Integer))


def downgrade():
    op.drop_column('users', 'confirmed')
