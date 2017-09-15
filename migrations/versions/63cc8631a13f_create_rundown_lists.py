"""create rundown list

Revision ID: 63cc8631a13f
Revises: 12923d2a24bf
Create Date: 2017-09-14 12:07:59.395613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63cc8631a13f'
down_revision = '12923d2a24bf'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('rundown_lists',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('description', sa.String(255)),
		sa.Column('time_start', sa.DateTime),
		sa.Column('time_end', sa.DateTime),
		sa.Column('location', sa.String(255)),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
	op.drop_table('rundown_lists')
