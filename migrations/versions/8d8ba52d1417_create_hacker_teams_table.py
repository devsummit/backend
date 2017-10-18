"""create_hacker_teams_table

Revision ID: 8d8ba52d1417
Revises: 590e64b96673
Create Date: 2017-10-17 17:43:28.206594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d8ba52d1417'
down_revision = '590e64b96673'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('hacker_teams',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('name', sa.String(60)),
        sa.Column('logo', sa.String(180)),
        sa.Column('project_name', sa.String(60)),
        sa.Column('project_url', sa.String(250)),
        sa.Column('theme', sa.String(60)),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime)
		)


def downgrade():
    op.drop_table('hacker_teams')
