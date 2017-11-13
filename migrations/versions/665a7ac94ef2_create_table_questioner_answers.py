"""create table questioner_answers

Revision ID: 665a7ac94ef2
Revises: 7ba92c15782e
Create Date: 2017-11-13 12:36:26.636771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '665a7ac94ef2'
down_revision = '7ba92c15782e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('questioner_answers',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('user_id', sa.Integer, sa.ForeignKey(
                        'users.id', ondelete='CASCADE')),
                    sa.Column('questioner_id', sa.Integer, sa.ForeignKey(
                        'questioners.id', ondelete='CASCADE')),
                    sa.Column('answers', sa.Text),
                    sa.Column('created_at', sa.DateTime),
                    sa.Column('updated_at', sa.DateTime)
                    )


def downgrade():
    op.drop_table('questioner_answers')
