"""empty message

Revision ID: 0ba15ddf5053
Revises: 2013e180c438
Create Date: 2019-11-13 17:26:36.584040

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0ba15ddf5053'
down_revision = '2013e180c438'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('milestone', sa.Column('days_estimated', sa.String(length=255), nullable=True))
    op.alter_column('milestone', 'date_estimated',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('milestone', 'date_estimated',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('milestone', 'days_estimated')
    # ### end Alembic commands ###
