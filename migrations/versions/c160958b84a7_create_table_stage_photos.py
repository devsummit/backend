"""create table stage_photos

Revision ID: c160958b84a7
Revises: cf5c0ef7ceaa
Create Date: 2017-08-01 19:13:20.055092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c160958b84a7'
down_revision = 'cf5c0ef7ceaa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('stage_photos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('stage_id', sa.Integer, sa.ForeignKey(
            'stages.id', ondelete='CASCADE')),
        sa.Column('url', sa.String(255)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        )


def downgrade():
    op.drop_table('stage_photos')
