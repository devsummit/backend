"""create notifications

Revision ID: 48e2ade3fa52
Revises: 543ed2ee3191
Create Date: 2017-09-16 12:50:41.965545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48e2ade3fa52'
down_revision = '543ed2ee3191'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('notifications',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('sender_user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('receiver_user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('message', sa.Text),
		sa.Column('attachment', sa.String(255)),
		sa.Column('type', sa.String(80)),
		sa.Column('status', sa.String(80)),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
	)


def downgrade():
    op.drop_table('notifications')
