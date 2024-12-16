"""add column media_tbl

Revision ID: c732de9256ef
Revises: 98fed8e8a22c
Create Date: 2024-12-16 16:34:06.602298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c732de9256ef'
down_revision = '98fed8e8a22c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media_tbl')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media_tbl',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('group_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('path', sa.VARCHAR(length=50), nullable=True),
    sa.Column('type', sa.VARCHAR(length=50), nullable=False),
    sa.Column('file_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('filename', sa.VARCHAR(length=255), nullable=True),
    sa.ForeignKeyConstraint(['group_name'], ['text_tbl.group_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
