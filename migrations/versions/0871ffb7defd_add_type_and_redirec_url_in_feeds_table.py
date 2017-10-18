"""add_type_and_redirec_url_in_feeds_table

Revision ID: 0871ffb7defd
Revises: b1dfd323d88f
Create Date: 2017-10-03 11:00:10.131941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0871ffb7defd'
down_revision = 'b1dfd323d88f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('feeds', sa.Column('type', sa.String(40)))
    op.add_column('feeds', sa.Column('redirect_url', sa.String(40)))
    op.add_column('feeds', sa.Column('sponsor_id', sa.Integer))


def downgrade():
    op.drop_column('feeds', 'type')
    op.drop_column('feeds', 'redirect_url')
    op.drop_column('feeds', 'sponsor_id')


    
    
    
