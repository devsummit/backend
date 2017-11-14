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
    op.add_column('beacons', sa.Column('type', sa.String(120)))
    op.add_column('beacons', sa.Column('description', sa.Text))
    op.add_column('beacons', sa.Column('type_id', sa.String(255)))
    op.add_column('beacons', sa.Column('minor', sa.String(255)))
    op.alter_column('beacons', 'code', existing_type=sa.String(255), nullable=False, new_column_name='major')


def downgrade():
    op.drop_column('beacons', 'type')
    op.drop_column('beacons', 'type_id')
    op.drop_column('beacons', 'description')
    op.drop_column('beacons', 'minor')
    op.alter_column('beacons', 'major', existing_type=sa.String(255), nullable=False, new_column_name='code')
