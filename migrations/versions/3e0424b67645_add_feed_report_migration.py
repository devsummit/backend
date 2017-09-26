"""add feed-report migration

Revision ID: 3e0424b67645
Revises: f4cc2d8278b3
Create Date: 2017-09-26 17:34:05.868226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e0424b67645'
down_revision = 'f4cc2d8278b3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'feed_reports',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer,
            sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('type', sa.String(255)),
        sa.Column('feed_id', sa.Integer, sa.ForeignKey('feeds.id', ondelete='CASCADE')),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

def downgrade():
    op.drop_table('feed_reports')
