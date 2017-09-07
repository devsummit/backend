"""create user table

Revision ID: 1314685ec5c0
Revises: aebf5ba482d6
Create Date: 2017-07-31 16:48:19.146630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1314685ec5c0'
down_revision = 'aebf5ba482d6'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('users',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('first_name', sa.String(120)),
		sa.Column('last_name', sa.String(120)),
		sa.Column('email', sa.String),
		sa.Column('username', sa.String(40), unique=True),
		sa.Column('email', sa.String(80), unique=True),
		sa.Column('password', sa.String(255)),
		sa.Column('social_id', sa.String(255)),
		sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
	op.drop_table('users')
