"""create client table

Revision ID: e431e5b0f9c3
Revises: 55d9b9bc9d9c
Create Date: 2017-08-13 11:54:39.019025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e431e5b0f9c3'
down_revision = '55d9b9bc9d9c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('clients',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('app_name', sa.String, unique=True),
                    sa.Column('client_secret', sa.String),
                    sa.Column('client_id', sa.String),
                    sa.Column('created_at', sa.DateTime),
                    sa.Column('updated_at', sa.DateTime)
                    )


def downgrade():
    op.drop_table('clients')
