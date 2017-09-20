"""create booth_gallery table

Revision ID: 52208163ddf7
Revises: 3f26380bd3b6
Create Date: 2017-09-19 12:35:55.984145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52208163ddf7'
down_revision = '3f26380bd3b6'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('booth_gallery',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('booth_id', sa.Integer, sa.ForeignKey('booths.id')),
    sa.Column('url', sa.String(255)),
    sa.Column('created_at', sa.DateTime),
    sa.Column('updated_at', sa.DateTime),
    )


def downgrade():
    op.drop_table('booth_gallery')
