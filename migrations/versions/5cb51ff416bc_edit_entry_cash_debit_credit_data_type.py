"""edit_entry_cash_debit_credit_data_type

Revision ID: 5cb51ff416bc
Revises: 4bb2073a8f01
Create Date: 2017-09-26 19:03:57.554231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cb51ff416bc'
down_revision = '4bb2073a8f01'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'entry_cash_log', 'debit',
        existing_type=sa.Integer,
        type_=sa.Float
    )

    op.alter_column(
        'entry_cash_log', 'credit',
        existing_type=sa.Integer,
        type_=sa.Float
    )


def downgrade():
    op.alter_column(
        'entry_cash_log', 'debit',
        existing_type=sa.Float,
        type_=sa.Integer
    )

    op.alter_column(
        'entry_cash_log', 'credit',
        existing_type=sa.Float,
        type_=sa.Integer
    )
    