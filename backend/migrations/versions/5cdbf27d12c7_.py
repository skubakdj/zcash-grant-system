"""empty message

Revision ID: 5cdbf27d12c7
Revises: 6624244a249e
Create Date: 2020-02-21 13:36:10.910186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cdbf27d12c7'
down_revision = '6624244a249e'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.create_table('proposal_revision',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('proposal_id', sa.Integer(), nullable=False),
    sa.Column('proposal_archive_id', sa.Integer(), nullable=False),
    sa.Column('proposal_archive_parent_id', sa.Integer(), nullable=True),
    sa.Column('changes', sa.Text(), nullable=False),
    sa.Column('revision_index', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['proposal_archive_id'], ['proposal.id'], ),
    sa.ForeignKeyConstraint(['proposal_archive_parent_id'], ['proposal.id'], ),
    sa.ForeignKeyConstraint(['proposal_id'], ['proposal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('proposal_revision')
    # ### end Alembic commands ###
