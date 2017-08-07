"""create booths table

Revision ID: ae1088ec2272
Revises: c160958b84a7
Create Date: 2017-08-07 09:25:18.067447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae1088ec2272'
down_revision = 'c160958b84a7'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('booths',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('stage_id', sa.Integer, sa.ForeignKey('stages.id'), nullable=True),
		sa.Column('points', sa.Integer),
		sa.Column('summary', sa.String),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
    op.drop_table('booths')
