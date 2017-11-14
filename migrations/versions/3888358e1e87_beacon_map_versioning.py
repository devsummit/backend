"""beacon map versioning


Revision ID: 3888358e1e87
Revises: 085673d555ba
Create Date: 2017-11-14 14:31:08.254158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3888358e1e87'
down_revision = '085673d555ba'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'beacon_map_version',
        sa.Column('version', sa.Integer, primary_key=True)
    )


def downgrade():
    op.drop_table('beacon_map_version')
