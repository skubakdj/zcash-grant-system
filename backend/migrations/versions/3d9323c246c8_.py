"""empty message

Revision ID: 3d9323c246c8
Revises: c2ccca4545b0
Create Date: 2019-11-05 17:39:17.830749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d9323c246c8'
down_revision = 'c2ccca4545b0'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ccr', sa.Column('target', sa.String(length=255), nullable=True))
    op.drop_column('ccr', 'bounty')
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ccr', sa.Column('bounty', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('ccr', 'target')
    # ### end Alembic commands ###
