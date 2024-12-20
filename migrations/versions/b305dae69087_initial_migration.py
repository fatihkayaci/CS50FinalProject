"""Initial migration

Revision ID: b305dae69087
Revises: 5abf42e28f53
Create Date: 2024-12-19 11:08:38.365466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b305dae69087'
down_revision = '5abf42e28f53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tblfoods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=50), nullable=True),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('text', sa.String(length=5000), nullable=True),
    sa.Column('order_index', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tblfoods')
    # ### end Alembic commands ###
