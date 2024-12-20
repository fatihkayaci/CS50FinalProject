"""Initial migration

Revision ID: bd1eff1742f1
Revises: f4622e87e24a
Create Date: 2024-12-18 17:28:49.208570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd1eff1742f1'
down_revision = 'f4622e87e24a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tblfoods',
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
    op.drop_table('tblfoods')
    # ### end Alembic commands ###