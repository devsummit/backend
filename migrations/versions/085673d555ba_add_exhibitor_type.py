"""add exhibitor type

Revision ID: 085673d555ba
Revises: b92a4590bb11, 665a7ac94ef2, f70539a5afd7
Create Date: 2017-11-14 13:12:17.220921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '085673d555ba'
down_revision = ('b92a4590bb11', '665a7ac94ef2', 'f70539a5afd7')
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('booths', sa.Column('type', sa.String(120)))


def downgrade():
    op.drop_column('booths', 'type')
