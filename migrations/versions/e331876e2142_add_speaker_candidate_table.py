"""add speaker_candidate table

Revision ID: e331876e2142
Revises: 7d0a1665e3f5
Create Date: 2017-09-20 12:33:24.051227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e331876e2142'
down_revision = '7d0a1665e3f5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'speaker_candidates',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(255)),
        sa.Column('last_name', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('job', sa.String(255)),
        sa.Column('summary', sa.String(255)),
        sa.Column('stage', sa.String(255)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )

def downgrade():
    op.drop_table('speaker_candidates')
