"""Initial migration

Revision ID: 5b807ed81c3b
Revises: bd1eff1742f1
Create Date: 2024-12-18 17:46:14.973975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b807ed81c3b'
down_revision = 'bd1eff1742f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tblfoods')
    op.drop_table('tbltext')
    op.drop_table('tblmedia')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tblmedia',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('text_id', sa.INTEGER(), nullable=True),
    sa.Column('page_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('label', sa.VARCHAR(length=100), nullable=True),
    sa.Column('path', sa.VARCHAR(length=50), nullable=False),
    sa.Column('file_name', sa.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['text_id'], ['tbltext.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tbltext',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('id_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('text', sa.VARCHAR(length=5000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tblfoods',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('page_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('photopath', sa.VARCHAR(length=50), nullable=False),
    sa.Column('label', sa.VARCHAR(length=100), nullable=True),
    sa.Column('text', sa.VARCHAR(length=5000), nullable=True),
    sa.Column('order_index', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
