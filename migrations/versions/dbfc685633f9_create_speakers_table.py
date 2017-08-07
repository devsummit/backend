"""create speakers table

Revision ID: dbfc685633f9
Revises: 8ba67ec99bcb
Create Date: 2017-08-07 09:32:10.637468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbfc685633f9'
down_revision = '8ba67ec99bcb'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('speakers',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('summary', sa.String),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
    op.drop_table('speakers')
