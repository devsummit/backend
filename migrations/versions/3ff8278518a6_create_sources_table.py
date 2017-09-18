"""create_sources_table

Revision ID: 3ff8278518a6
Revises: 77e953519a64
Create Date: 2017-09-18 16:40:01.920745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ff8278518a6'
down_revision = '77e953519a64'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'sources',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('account_number', sa.Integer),
		sa.Column('bank', sa.String(40)),
		sa.Column('alias', sa.String(60)),	   
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime)
	)


def downgrade():
	op.drop_table('rundown_lists')
