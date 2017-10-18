"""create point_transaction_log table


Revision ID: 3ae3a27a9771
Revises: b1cb653806ab
Create Date: 2017-08-07 09:43:07.268924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ae3a27a9771'
down_revision = 'b1cb653806ab'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('point_transaction_log',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('booth_id', sa.Integer, sa.ForeignKey('booths.id')),
		sa.Column('attendee_id', sa.Integer, sa.ForeignKey('attendees.id')),
		sa.Column('amount', sa.Integer),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
	op.drop_table('point_transaction_log')
