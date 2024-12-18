"""Initial migration

Revision ID: c2d28339f58b
Revises: cf8f39ebc1ff
Create Date: 2024-12-18 14:49:46.213256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2d28339f58b'
down_revision = 'cf8f39ebc1ff'
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
    op.create_table('tblmedia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=50), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tblusers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tbltext',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photoid', sa.Integer(), nullable=True),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('page_name', sa.String(length=50), nullable=False),
    sa.Column('id_name', sa.String(length=50), nullable=False),
    sa.Column('text', sa.String(length=5000), nullable=True),
    sa.ForeignKeyConstraint(['photoid'], ['tblmedia.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('text_tbl')
    op.drop_table('media_tbl')
    op.drop_table('foods')
    op.drop_table('users_tbl')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_tbl',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('password', sa.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('foods',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('page_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('photopath', sa.VARCHAR(length=50), nullable=False),
    sa.Column('label', sa.VARCHAR(length=100), nullable=True),
    sa.Column('text', sa.VARCHAR(length=5000), nullable=True),
    sa.Column('order_index', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('media_tbl',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('group_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('path', sa.VARCHAR(length=50), nullable=False),
    sa.Column('file_name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('active', sa.BOOLEAN(), nullable=False),
    sa.Column('order_index', sa.INTEGER(), nullable=False),
    sa.Column('label', sa.VARCHAR(length=100), nullable=True),
    sa.Column('page_name', sa.VARCHAR(length=50), server_default=sa.text("('')"), nullable=True),
    sa.ForeignKeyConstraint(['group_name'], ['text_tbl.group_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('text_tbl',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('group_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('id_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('text', sa.VARCHAR(length=5000), nullable=True),
    sa.Column('label', sa.VARCHAR(length=100), nullable=True),
    sa.Column('page_name', sa.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('tbltext')
    op.drop_table('tblusers')
    op.drop_table('tblmedia')
    op.drop_table('tblfoods')
    # ### end Alembic commands ###
