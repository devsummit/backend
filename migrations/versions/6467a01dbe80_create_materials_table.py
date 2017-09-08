"""create materials table

Revision ID: 6467a01dbe80
Revises: dbfc685633f9
Create Date: 2017-08-07 09:34:14.458307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6467a01dbe80'
down_revision = 'dbfc685633f9'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table('materials',
		sa.Column('id', sa.Integer, primary_key=True),
		sa.Column('speaker_id', sa.Integer, sa.ForeignKey('speakers.id')),
		sa.Column('material', sa.String(255)),
		sa.Column('created_at', sa.DateTime),
		sa.Column('updated_at', sa.DateTime),
		)


def downgrade():
    op.drop_table('materials')
