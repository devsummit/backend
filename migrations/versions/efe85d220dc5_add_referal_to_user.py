"""add referal to user

Revision ID: efe85d220dc5
Revises: 2ad9bae1b2c3, f962a2941f5b, 0ed8801fa88a
Create Date: 2017-10-13 16:35:17.037736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efe85d220dc5'
down_revision = ('2ad9bae1b2c3', 'f962a2941f5b', '0ed8801fa88a')
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('referal_count', sa.Integer))
    op.add_column('users', sa.Column('have_refered', sa.Integer))
    op.alter_column('users', 'referer', 
        new_column_name='referal',
        existing_type=sa.String(40))


def downgrade():
    op.drop_column('users', 'referal_count')
    op.drop_column('users', 'have_refered')
    op.alter_column('users', 'referal', new_column_name='referer', existing_type=sa.String(40))
