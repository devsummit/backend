"""create user_booth table

Revision ID: 3f26380bd3b6
Revises: caa004f8af83
Create Date: 2017-09-19 12:21:39.984790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f26380bd3b6'
down_revision = 'caa004f8af83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_booth', 
      sa.Column('id', sa.Integer, primary_key=True),
      sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
      sa.Column('booth_id', sa.Integer, sa.ForeignKey('booths.id')),
      sa.Column('created_at', sa.DateTime),
      sa.Column('updated_at', sa.DateTime),
      )


def downgrade():
    op.drop_table('user_booth')
