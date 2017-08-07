"""create schedules table

Revision ID: 0db2d38988c5
Revises: 4e5eaa7314eb
Create Date: 2017-08-07 09:36:29.573678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0db2d38988c5'
down_revision = '4e5eaa7314eb'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('schedules',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('event_id', sa.Integer, sa.ForeignKey('events.id')),
		sa.Column('stage_id', sa.Integer, sa.ForeignKey('stages.id')),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
	op.drop_table('schedules')
