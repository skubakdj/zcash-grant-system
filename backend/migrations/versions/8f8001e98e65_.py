"""empty message

Revision ID: 8f8001e98e65
Revises: 2721189b0c8f
Create Date: 2020-02-07 12:42:57.248894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f8001e98e65'
down_revision = '2721189b0c8f'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposal', sa.Column('changes_requested_discussion', sa.Boolean(), nullable=True))
    op.add_column('proposal', sa.Column('changes_requested_discussion_reason', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('proposal', 'changes_requested_discussion_reason')
    op.drop_column('proposal', 'changes_requested_discussion')
    # ### end Alembic commands ###