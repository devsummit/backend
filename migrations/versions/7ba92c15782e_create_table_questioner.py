"""create table questioner

Revision ID: 7ba92c15782e
Revises: 645494c3895d
Create Date: 2017-11-13 12:28:36.981820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ba92c15782e'
down_revision = '645494c3895d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('questioners',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('booth_id', sa.Integer, sa.ForeignKey(
                        'booths.id', ondelete='CASCADE')),
                    sa.Column('question', sa.Text),
                    sa.Column('created_at', sa.DateTime),
                    sa.Column('updated_at', sa.DateTime)
                    )


def downgrade():
    op.drop_table('questioners')
