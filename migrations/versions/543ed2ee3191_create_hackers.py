"""create hackers

Revision ID: 543ed2ee3191
Revises: ce19962c2422
Create Date: 2017-09-16 12:50:31.342189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '543ed2ee3191'
down_revision = 'ce19962c2422'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('hackers',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
		sa.Column('team_id', sa.Integer,
            sa.ForeignKey('hacker_teams.id')),
		sa.Column('lead', sa.Boolean),
		sa.Column('summary', sa.String(255)),
		sa.Column('points', sa.Integer),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
	)


def downgrade():
    op.drop_table('hackers')
