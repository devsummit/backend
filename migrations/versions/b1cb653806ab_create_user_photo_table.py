"""create user_photo table

Revision ID: b1cb653806ab
Revises: 6cdc598b190b
Create Date: 2017-08-07 09:40:10.540575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1cb653806ab'
down_revision = '6cdc598b190b'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('user_photo',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('url', sa.String(255)),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
	op.drop_table('user_photo')
