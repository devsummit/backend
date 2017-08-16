"""create newsletters table

Revision ID: d0f006ed40b0
Revises: e431e5b0f9c3
Create Date: 2017-08-11 18:06:32.159516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0f006ed40b0'
down_revision = 'e431e5b0f9c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('newsletters',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('email', sa.String, unique=True),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
    op.drop_table('newsletters')
