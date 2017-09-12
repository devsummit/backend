"""create sponsor table

Revision ID: b328dd38d1fa
Revises: 4a836f32b170
Create Date: 2017-09-12 22:42:14.239740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b328dd38d1fa'
down_revision = '4a836f32b170'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sponsors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(120)),
        sa.Column('email', sa.String(120)),
        sa.Column('phone', sa.String(80)),
        sa.Column('note', sa.Text()),
        sa.Column('type', sa.String(40)),
        sa.Column('stage', sa.String(40)),
        sa.Column('attachment', sa.String(255)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('sponsors')
