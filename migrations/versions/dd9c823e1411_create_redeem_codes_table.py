"""create redeem codes table

Revision ID: dd9c823e1411
Revises: caa004f8af83
Create Date: 2017-09-18 21:31:13.804208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd9c823e1411'
down_revision = 'caa004f8af83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'redeem_codes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('codeable_type', sa.String(40)),
        sa.Column('codeable_id', sa.String(40)),
        sa.Column('code', sa.String(6), unique=True),
        sa.Column('count', sa.Integer()),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('redeem_codes')
