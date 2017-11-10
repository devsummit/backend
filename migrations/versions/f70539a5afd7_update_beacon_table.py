"""update beacon table

Revision ID: f70539a5afd7
Revises: 645494c3895d
Create Date: 2017-11-10 16:19:18.492547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f70539a5afd7'
down_revision = '645494c3895d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('beacons', sa.Column('action', sa.String(120)))
    op.add_column('beacons', sa.Column('identifier', sa.String(255)))


def downgrade():
    op.drop_column('beacons', 'identifier')
    op.drop_column('beacons', 'action')
    
