"""Initial migration

Revision ID: cf8f39ebc1ff
Revises: db0e866378ab
Create Date: 2024-12-18 09:12:51.980761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf8f39ebc1ff'
down_revision = 'db0e866378ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('foods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('page_name', sa.String(length=50), nullable=False),
    sa.Column('photopath', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('text', sa.String(length=5000), nullable=True),
    sa.Column('order_index', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('foods')
    # ### end Alembic commands ###