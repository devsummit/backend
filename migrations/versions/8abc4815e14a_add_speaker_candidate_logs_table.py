"""add speaker_candidate_logs table

Revision ID: 8abc4815e14a
Revises: e331876e2142
Create Date: 2017-09-21 01:02:39.555106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8abc4815e14a'
down_revision = 'e331876e2142'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'speaker_candidate_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('candidate_id', sa.Integer,
                  sa.ForeignKey('speaker_candidates.id', ondelete='CASCADE')),
        sa.Column('message', sa.String(255)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('speaker_candidate_logs')
