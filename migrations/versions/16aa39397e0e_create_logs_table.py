"""create logs table


Revision ID: 16aa39397e0e
Revises: 66237493cf86
Create Date: 2017-10-18 15:05:16.692943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16aa39397e0e'
down_revision = '66237493cf86'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('logs')
