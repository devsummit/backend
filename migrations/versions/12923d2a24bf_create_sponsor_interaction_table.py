"""create sponsor interaction table

Revision ID: 12923d2a24bf
Revises: b328dd38d1fa
Create Date: 2017-09-12 22:42:40.643509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12923d2a24bf'
down_revision = 'b328dd38d1fa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sponsor_interaction_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sponsor_id', sa.Integer,
            sa.ForeignKey('sponsors.id', ondelete='CASCADE')),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('sponsor_interaction_log')
