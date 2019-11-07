"""empty message

Revision ID: 39729502e0c5
Revises: 7fea7427e9d6
Create Date: 2019-11-07 17:58:36.592816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39729502e0c5'
down_revision = '7fea7427e9d6'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_settings', sa.Column('tip_jar_address', sa.String(length=255), nullable=True))
    op.add_column('user_settings', sa.Column('tip_jar_view_key', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_settings', 'tip_jar_view_key')
    op.drop_column('user_settings', 'tip_jar_address')
    # ### end Alembic commands ###
