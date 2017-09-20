"""create notification table

Revision ID: 7d0a1665e3f5
Revises: 0b20a93243e4
Create Date: 2017-09-19 02:17:15.309841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d0a1665e3f5'
down_revision = '0b20a93243e4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('receiver_uid', sa.Integer,
            sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('sender_uid', sa.Integer,
            sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('message', sa.Text),
        sa.Column('type', sa.String(120)),
        sa.Column('attachment', sa.String(255)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )



def downgrade():
    op.drop_table('notifications')
