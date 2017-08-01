"""create access_token table

Revision ID: 79d78e481ff5
Revises: 1314685ec5c0
Create Date: 2017-07-31 20:54:35.517706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79d78e481ff5'
down_revision = '1314685ec5c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'access_tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer,
            sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('access_token', sa.String),
        sa.Column('refresh_token', sa.String),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.drop_table('access_tokens')
