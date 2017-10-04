"""create_sponsor_templates_table

Revision ID: b9dc4f84ae83
Revises: 0871ffb7defd
Create Date: 2017-10-03 16:48:01.280663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9dc4f84ae83'
down_revision = '0871ffb7defd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sponsor_templates',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sponsor_id', sa.Integer, sa.ForeignKey('sponsors.id')),
        sa.Column('message', sa.Text),
        sa.Column('attachment', sa.String(255)),
        sa.Column('redirect_url', sa.String(255)),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    op.drop_table('sponsor_templates')
