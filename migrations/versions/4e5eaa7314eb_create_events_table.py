"""create events table

Revision ID: 4e5eaa7314eb
Revises: 6467a01dbe80
Create Date: 2017-08-07 09:35:12.505641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e5eaa7314eb'
down_revision = '6467a01dbe80'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('events',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('title', sa.String),
		sa.Column('information', sa.String),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
    op.drop_table('events')
