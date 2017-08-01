"""create table stages

Revision ID: efa23ae7975d
Revises: 48e1845a4774
Create Date: 2017-08-01 19:12:39.671198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efa23ae7975d'
down_revision = '48e1845a4774'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('stages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('stage_type', sa.String),
        sa.Column('information', sa.String),
        sa.Column('timestamps', sa.DateTime)
    )

def downgrade():
    op.drop_table('stages')

