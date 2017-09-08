"""create role table


Revision ID: aebf5ba482d6
Revises:
Create Date: 2017-07-31 16:49:51.099091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aebf5ba482d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'roles',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('name', sa.String(255)),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime)
		)


def downgrade():
	op.drop_table('roles')
