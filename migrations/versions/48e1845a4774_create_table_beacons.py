"""create table beacons

Revision ID: 48e1845a4774
Revises: 79d78e481ff5
Create Date: 2017-08-01 19:10:24.737442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48e1845a4774'
down_revision = '7df08705de21'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('beacons',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('code', sa.String(255)),
                    sa.Column('created_at', sa.DateTime),
                    sa.Column('updated_at', sa.DateTime)
                    )


def downgrade():
    op.drop_table('beacons')
