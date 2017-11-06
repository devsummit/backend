"""add comment table

Revision ID: 9900649d5aca
Revises: 2004f48169b4
Create Date: 2017-11-06 12:25:41.723107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9900649d5aca'
down_revision = '2004f48169b4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('feed_id', sa.Integer),
        sa.Column('content', sa.Text),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.drop_table('comments')
