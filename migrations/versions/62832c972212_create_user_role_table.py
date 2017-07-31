"""create user_role table

Revision ID: 62832c972212
Revises: aebf5ba482d6
Create Date: 2017-07-31 16:51:40.009498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62832c972212'
down_revision = 'aebf5ba482d6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    	'user_role',
    	sa.Column('user_id', sa.Integer, 
            sa.ForeignKey('users.id', ondelete='CASCADE')),
    	sa.Column('role_id', sa.Integer,
    		sa.ForeignKey('roles.id')),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime)
    	)


def downgrade():
    op.drop_table('user_role')
