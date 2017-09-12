"""create partners table

Revision ID: 4a836f32b170
Revises: f66e7f85d4e7
Create Date: 2017-09-12 01:25:52.387905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a836f32b170'
down_revision = 'ae0efd1cf5c1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'partners',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(120)),
        sa.Column('email', sa.String(120)),
        sa.Column('type', sa.String(40)),
        sa.Column('photo', sa.String(255)),
        sa.Column('website', sa.String(120)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('partners')
