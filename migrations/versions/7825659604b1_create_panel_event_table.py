"""create panel_event table

Revision ID: 7825659604b1
Revises: 90062c172360, b9dc4f84ae83
Create Date: 2017-10-04 18:21:09.956396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7825659604b1'
down_revision = ('90062c172360', 'b9dc4f84ae83')
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
        'panel_event',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('event_id', sa.Integer,
        	sa.ForeignKey('events.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer,
        	sa.ForeignKey('users.id', ondelete='CASCADE'))
    )

def downgrade():
    op.drop_table('panel_event')
