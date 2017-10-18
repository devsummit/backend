"""create attendees table

Revision ID: 8ba67ec99bcb
Revises: ae1088ec2272
Create Date: 2017-08-07 09:30:52.038219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ba67ec99bcb'
down_revision = 'ae1088ec2272'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('attendees',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('points', sa.Integer),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
    op.drop_table('attendees')
