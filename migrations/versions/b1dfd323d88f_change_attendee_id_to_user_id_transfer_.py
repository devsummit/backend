"""change attendee_id to user_id transfer log

Revision ID: b1dfd323d88f
Revises: 9171ee250063
Create Date: 2017-09-28 18:40:22.475680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1dfd323d88f'
down_revision = '9171ee250063'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('point_transaction_log_ibfk_2', 'point_transaction_log', 'foreignkey')
    op.drop_column('point_transaction_log', 'attendee_id')
    op.add_column('point_transaction_log', sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')))


def downgrade():
	op.drop_constraint('point_transaction_log_ibfk_2', 'point_transaction_log', 'foreignkey')
	op.drop_column('point_transaction_log', 'user_id')
	op.add_column('point_transaction_log', sa.Column('attendee_id', sa.Integer, sa.ForeignKey('attendees.id', ondelete='CASCADE')))
