"""empty message

Revision ID: 7fea7427e9d6
Revises: f24d53f211ef
Create Date: 2019-10-24 12:18:39.734758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fea7427e9d6'
down_revision = 'f24d53f211ef'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rfp_liker',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('rfp_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['rfp_id'], ['rfp.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('proposal_liker',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('proposal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['proposal_id'], ['proposal.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('comment_liker',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_liker')
    op.drop_table('proposal_liker')
    op.drop_table('rfp_liker')
    # ### end Alembic commands ###
