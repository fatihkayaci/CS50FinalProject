"""Initial migration

Revision ID: 3444444dff77
Revises: 08110a5c6717
Create Date: 2024-12-14 23:53:17.897078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3444444dff77'
down_revision = '08110a5c6717'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text_tbl',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_name', sa.String(length=50), nullable=False),
    sa.Column('text', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_tbl',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('password', sa.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users_tbl')
    op.drop_table('text_tbl')
    # ### end Alembic commands ###
