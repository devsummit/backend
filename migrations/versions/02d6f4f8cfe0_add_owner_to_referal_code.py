"""add owner to referal code

Revision ID: 02d6f4f8cfe0
Revises: 47d9c68393ed
Create Date: 2017-10-31 12:39:26.939401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02d6f4f8cfe0'
down_revision = '47d9c68393ed'
branch_labels = None
depends_on = None


def upgrade():
	op.drop_column('referals', 'owner')
	op.create_table(
        'referal_owner',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('referalable_type', sa.String(100)),
        sa.Column('referalable_id', sa.Integer),
        sa.Column('referal_id', sa.Integer),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.add_column('referals', sa.Column('owner', sa.String(255)))
    op.drop_table('referal_owner')
