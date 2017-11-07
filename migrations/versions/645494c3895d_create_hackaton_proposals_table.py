"""create hackaton proposals table

Revision ID: 645494c3895d
Revises: 9900649d5aca
Create Date: 2017-11-06 21:25:10.875079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '645494c3895d'
down_revision = '9900649d5aca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hackaton_proposals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('github_link', sa.String(255)),
        sa.Column('order_id', sa.String(255)),
        sa.Column('status', sa.String(255)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )



def downgrade():
    op.drop_table('hackaton_proposals')
