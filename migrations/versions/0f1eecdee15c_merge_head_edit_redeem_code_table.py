"""merge head edit redeem code table

Revision ID: 0f1eecdee15c
Revises: 540bd35ba67d, 52208163ddf7, dd9c823e1411, 4a97ebacb049, 7d0a1665e3f5
Create Date: 2017-09-20 10:32:00.272430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f1eecdee15c'
down_revision = ('540bd35ba67d', '52208163ddf7', 'dd9c823e1411', '4a97ebacb049', '7d0a1665e3f5')
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('redeem_codes', 'count')
    op.add_column(
        'redeem_codes',
         sa.Column('used', sa.Boolean(), server_default=sa.schema.DefaultClause("0"), 
         nullable=False)
    )


def downgrade():
    op.add_column('redeem_codes', sa.Column('count', sa.Integer))
    op.drop_column('redeem_codes', 'used')