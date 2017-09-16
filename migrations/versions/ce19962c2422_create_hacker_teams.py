"""create hacker_teams

Revision ID: ce19962c2422
Revises: 77e953519a64
Create Date: 2017-09-16 12:50:15.566522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce19962c2422'
down_revision = '77e953519a64'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('hacker_teams',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('team_name', sa.String(255)),
		sa.Column('city', sa.String(120)),
		sa.Column('project_name', sa.String(255)),
		sa.Column('points', sa.Integer),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
	)



def downgrade():
    op.drop_table('hacker_teams')
