"""Initial migration

Revision ID: edc75c2ad912
Revises: 9839f659ee91
Create Date: 2024-12-18 22:11:26.660341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edc75c2ad912'
down_revision = '9839f659ee91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tblcomputerfiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('videocard', sa.String(length=100), nullable=True),
    sa.Column('mothercard', sa.String(length=100), nullable=True),
    sa.Column('freez', sa.String(length=100), nullable=True),
    sa.Column('mouse', sa.String(length=100), nullable=True),
    sa.Column('headphone', sa.String(length=100), nullable=True),
    sa.Column('processor', sa.String(length=100), nullable=True),
    sa.Column('ram', sa.String(length=100), nullable=True),
    sa.Column('screen', sa.String(length=100), nullable=True),
    sa.Column('keyboard', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tblcomputerfiles')
    # ### end Alembic commands ###
