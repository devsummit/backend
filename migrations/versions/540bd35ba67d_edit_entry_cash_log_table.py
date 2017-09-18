"""edit_entry_cash_log_table

Revision ID: 540bd35ba67d
Revises: 3ff8278518a6
Create Date: 2017-09-18 16:46:20.885067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '540bd35ba67d'
down_revision = '3ff8278518a6'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('entry_cash_log', 'amount')
    op.add_column('entry_cash_log',
                  sa.Column('source_id', sa.Integer, sa.ForeignKey('sources.id')))
    op.add_column('entry_cash_log',
                  sa.Column('debit', sa.Integer))
    op.add_column('entry_cash_log',
                  sa.Column('credit', sa.Integer))


def downgrade():
    op.drop_column('entry_cash_log', 'credit')
    op.drop_column('entry_cash_log', 'debit')
    op.drop_column('entry_cash_log', 'source_id')
    op.add_column('entry_cash_log', sa.Integer)
