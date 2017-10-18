"""create_user_hackers_table

Revision ID: 66237493cf86
Revises: 8d8ba52d1417
Create Date: 2017-10-17 17:50:27.896561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66237493cf86'
down_revision = '8d8ba52d1417'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('user_hackers',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('hacker_team_id', sa.Integer, sa.ForeignKey('hacker_teams.id')),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime)
		)

def downgrade():
    op.drop_table('user_hackers')