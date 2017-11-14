"""add url field to booth

Revision ID: b92a4590bb11
Revises: 4dad14979537
Create Date: 2017-11-13 15:45:55.587290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b92a4590bb11'
down_revision = '4dad14979537'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('booths', sa.Column('url', sa.String(255)))


def downgrade():
    op.drop_column('booths', 'url')
