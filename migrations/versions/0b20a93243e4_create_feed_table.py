"""create feed table

Revision ID: 0b20a93243e4
Revises: caa004f8af83
Create Date: 2017-09-19 00:36:30.274351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b20a93243e4'
down_revision = 'caa004f8af83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'feeds',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer,
            sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('message', sa.Text),
        sa.Column('attachment', sa.String(255)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('feeds')
