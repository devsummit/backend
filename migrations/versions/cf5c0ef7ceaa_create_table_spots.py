"""create table spots

Revision ID: cf5c0ef7ceaa
Revises: efa23ae7975d
Create Date: 2017-08-01 19:13:03.381935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf5c0ef7ceaa'
down_revision = 'efa23ae7975d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('spots',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('beacon_id', sa.Integer, sa.ForeignKey(
                        'beacons.id', ondelete='CASCADE')),
                    sa.Column('stage_id', sa.Integer, sa.ForeignKey(
                        'stages.id', ondelete='CASCADE')),
                    sa.Column('created_at', sa.DateTime),
                    sa.Column('updated_at', sa.DateTime)
                    )


def downgrade():
    op.drop_table('spots')
