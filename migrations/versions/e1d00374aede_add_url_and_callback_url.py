"""add url and callback url

Revision ID: e1d00374aede
Revises: 2ad9bae1b2c3, 0ed8801fa88a, f962a2941f5b
Create Date: 2017-10-13 16:40:07.995737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1d00374aede'
down_revision = ('2ad9bae1b2c3', '0ed8801fa88a', 'f962a2941f5b')
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sponsors', sa.Column('url', sa.String(255)))
    op.add_column('sponsors', sa.Column('callback_url', sa.String(255)))
    

def downgrade():
    op.drop_column('sponsors', 'url')
    op.drop_column('sponsors', 'callback_url')
