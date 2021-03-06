"""empty message

Revision ID: 8ce33ae5d7f4
Revises: e8b721202138
Create Date: 2020-11-26 23:53:40.341288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ce33ae5d7f4'
down_revision = 'e8b721202138'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('search',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('search_type', sa.Integer(), nullable=False),
    sa.Column('step', sa.Integer(), nullable=True),
    sa.Column('unit', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('search')
    # ### end Alembic commands ###
