"""drop unique_column_code_redeem_codes

Revision ID: 4bb2073a8f01
Revises: ab469fe11442
Create Date: 2017-09-26 17:21:50.897085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bb2073a8f01'
down_revision = 'ab469fe11442'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("code", "redeem_codes", type_='unique')


def downgrade():
    op.create_unique_constraint(None, 'redeem_codes', ['code'])
    
