"""create booth checkin table

Revision ID: 4dad14979537
Revises: 645494c3895d
Create Date: 2017-11-13 11:35:32.798690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dad14979537'
down_revision = '645494c3895d'
branch_labels = None
depends_on = None


def upgrade():
	# booth table should be named exhibitors, therefore booth here
	# mean the place, could be sponsor, exhibitor or community partners
    op.create_table(
        'booth_checkins',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer,
            sa.ForeignKey('users.id')),
        sa.Column('booth_type', sa.String(40)),
        sa.Column('booth_id', sa.String(40)),
        sa.Column('speed_dating', sa.Boolean(), server_default=sa.schema.DefaultClause("0")),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
        )


def downgrade():
    op.drop_table('booth_checkins')
