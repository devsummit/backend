"""create_user_feedback_table

Revision ID: 88c366de3537
Revises: 66237493cf86
Create Date: 2017-10-18 19:02:32.838541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88c366de3537'
down_revision = '66237493cf86'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('user_feedbacks',
		sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('content', sa.String(255)),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime)
		)


def downgrade():
	op.drop_table('user_feedbacks')

