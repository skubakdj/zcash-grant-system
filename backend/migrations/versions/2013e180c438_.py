"""empty message

Revision ID: 2013e180c438
Revises: 7fea7427e9d6
Create Date: 2019-11-05 15:53:00.533347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2013e180c438'
down_revision = '7fea7427e9d6'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('proposal', 'category',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('rfp', 'category',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rfp', 'category',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('proposal', 'category',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###