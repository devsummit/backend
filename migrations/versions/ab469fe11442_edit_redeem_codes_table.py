"""edit redeem_codes_table

Revision ID: ab469fe11442
Revises: f4cc2d8278b3
Create Date: 2017-09-26 16:51:10.329463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab469fe11442'
down_revision = 'f4cc2d8278b3'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'redeem_codes', 'code',
        existing_type=sa.String(6),
        type_=sa.String(40),
        unique=True
        )


def downgrade():
    op.alter_column(
        'redeem_codes', 'code',
        existing_type=sa.String(40),
        type_=sa.String(6),
        unique=True
        )
